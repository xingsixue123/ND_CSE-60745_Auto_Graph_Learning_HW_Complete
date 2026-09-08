#!/usr/bin/env python3
"""fw -- the homework pipeline driver.

Commands the *user* runs on the host:

    fw run                    start a whole job (ingest + spawn master, then wait)
    fw init                   just create the job dir and ingest, without spawning
    fw status                 what is going on

Commands the *master agent* runs from inside its sandbox:

    fw spawn-worker <pid>     run one problem to convergence (blocking)
    fw respawn-worker <pid>   throw away a problem's work and start it again
    fw submit                 hand the assembled answer to the master validator

Everything that must not be left to a model's judgement lives here rather than in a
prompt: which directories an agent can write to, that workers run one at a time, and
that a loop stops after its cap instead of running forever.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import signal
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sandbox  # noqa: E402
from ingest import ingest as run_ingest  # noqa: E402

ROOT = Path("/home/xing/project/auto_hw_complete")
FRAMEWORK = ROOT / "framework"
PROMPTS = FRAMEWORK / "prompts"
INPUT = ROOT / "input"
SPECS = ROOT / "specs.md"
PLAYGROUND = ROOT / "playground"
OUTPUT = ROOT / "output"

CONFIG = json.loads((FRAMEWORK / "config.json").read_text())


# ----------------------------------------------------------------- job plumbing

def now() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def job_id() -> str:
    """A readable slug plus a short hash, so runs are findable by eye."""
    names = sorted(p.name for p in INPUT.rglob("*") if p.is_file())
    seed = "\n".join(names) + (SPECS.read_text() if SPECS.exists() else "")
    h = hashlib.sha256(seed.encode()).hexdigest()[:6]
    slug = "hw"
    for n in names:
        m = re.search(r"([A-Za-z]{2,}\s*\d{3,})", n)
        if m:
            slug = re.sub(r"\s+", "", m.group(1)).lower()
            break
    return f"{slug}_{dt.datetime.now():%Y%m%d}_{h}"


def find_job() -> Path:
    if os.environ.get("HW_JOB_DIR"):
        return Path(os.environ["HW_JOB_DIR"])
    here = Path.cwd().resolve()
    for cand in [here, *here.parents]:
        if (cand / "state.json").is_file() and cand.parent == PLAYGROUND:
            return cand
    jobs = sorted((p for p in PLAYGROUND.iterdir()
                   if p.is_dir() and (p / "state.json").is_file()),
                  key=lambda p: p.stat().st_mtime)
    if not jobs:
        sys.exit("no job found; run `fw init` first")
    return jobs[-1]


def load_state(job: Path) -> dict:
    return json.loads((job / "state.json").read_text())


def save_state(job: Path, st: dict) -> None:
    (job / "state.json").write_text(json.dumps(st, indent=2))


class Heartbeat:
    """Log "still alive, still working" while an agent blocks.

    The master cannot log its own status every N minutes the way the spec asks,
    because `fw spawn-worker` blocks it for the whole duration of a problem.  So the
    driver does it instead -- which is also more honest, since it reports elapsed
    wall-clock the master could not observe from inside a blocked call.
    """

    def __init__(self, job: Path, phase: str, seconds: int):
        self.job, self.phase, self.seconds = job, phase, seconds
        self._stop = threading.Event()
        self._t = None

    def _run(self):
        start = time.time()
        while not self._stop.wait(self.seconds):
            mins = (time.time() - start) / 60
            line = f"[{now()}] HEARTBEAT {self.phase} running {mins:.0f} min\n"
            (self.job / "logs").mkdir(parents=True, exist_ok=True)
            with open(self.job / "logs" / "heartbeat.log", "a") as fh:
                fh.write(line)
            with open(self.job / "logs" / "run.log", "a") as fh:
                fh.write(line)

    def __enter__(self):
        self._t = threading.Thread(target=self._run, daemon=True)
        self._t.start()
        return self

    def __exit__(self, *exc):
        self._stop.set()


def classify(rc: int, res: str, data) -> str:
    """PASS / FAIL / ERROR.

    Treating every non-PASS output as FAIL is wrong and expensive: a validator that
    crashed burns a submission round AND feeds its own stack trace to the master as
    if it were a defect list.  A real verdict always carries a VERDICT: line; anything
    else is the harness failing, not the work.
    """
    if rc != 0 or data is None or data.get("is_error"):
        return "ERROR"
    if not re.search(r"VERDICT:\s*(PASS|FAIL)", res or ""):
        return "ERROR"
    return "PASS" if re.search(r"VERDICT:\s*PASS", res) else "FAIL"


def record_cost(job: Path, data, label: str) -> None:
    if not data:
        return
    cost = data.get("total_cost_usd") or 0.0
    st = load_state(job)
    st["cost_usd"] = round(st.get("cost_usd", 0.0) + cost, 4)
    save_state(job, st)
    log(job, f"{label}: ${cost:.2f} (job total ${st['cost_usd']:.2f})")


def log(job: Path, msg: str) -> None:
    (job / "logs").mkdir(parents=True, exist_ok=True)
    line = f"[{now()}] {msg}\n"
    with open(job / "logs" / "run.log", "a") as fh:
        fh.write(line)
    print(line.rstrip())


# ------------------------------------------------------------- prompt assembly

def read(p: Path) -> str:
    return p.read_text()


def system_prompt(role: str, level: str, runtime: dict) -> str:
    """env sheet + hard rules + shared level context + role + runtime facts.

    The two agents at a level get byte-identical env/rules/context sections; only the
    role section and the runtime block differ.  That symmetry is deliberate: a
    validator that knows less than the agent it audits cannot audit it.
    """
    parts = [
        read(FRAMEWORK / "env.md"),
        read(FRAMEWORK / "rules.md"),
        read(PROMPTS / f"context_{level}.md"),
        read(PROMPTS / f"{role}.md"),
        "# Runtime facts for this run\n\n" + "\n".join(
            f"- **{k}**: {v}" for k, v in runtime.items()),
    ]
    return "\n\n---\n\n".join(parts)


# ------------------------------------------------------------------- commands

def cmd_init(args) -> Path:
    # Ignore dotfiles: input/ carries a .gitkeep so the directory survives a clone,
    # and that must not read as "an assignment is present".
    if not INPUT.exists() or not any(f for f in INPUT.rglob("*")
                                     if f.is_file() and not f.name.startswith(".")):
        sys.exit(f"{INPUT} contains no assignment files -- drop the assignment in first")
    jid = job_id()
    job = PLAYGROUND / jid

    # job_id is deterministic in (date, input filenames, specs.md), so re-running
    # `fw run` on the same assignment on the same day lands on the same directory.
    # Re-initializing would overwrite state.json and lose every finished problem.
    if (job / "state.json").is_file() and not getattr(args, "fresh", False):
        st = load_state(job)
        done = sum(1 for v in st["problems"].values() if v["status"] == "done")
        sys.exit(
            f"job {jid} already exists ({done}/{len(st['problems'])} problems done, "
            f"{st['master_rounds']} submission(s) used).\n"
            f"  fw resume    continue it\n"
            f"  fw status    look at it\n"
            f"  fw run --fresh   throw it away and start over")
    out = OUTPUT / jid
    for d in (job / "problems", job / "validators", job / "validator",
              job / "logs", out / "final"):
        d.mkdir(parents=True, exist_ok=True)

    log(job, f"job {jid} created")
    log(job, "ingesting input ...")
    manifest = run_ingest(INPUT, job / "ingest")

    st = {
        "job": jid,
        "created": now(),
        "playground": str(job),
        "output": str(out),
        "problems": {},
        "problem_order": [],
        "master_rounds": 0,
        "status": "initialized",
        "documents": [e["name"] for e in manifest["entries"]
                      if e["kind"] == "document"],
    }
    save_state(job, st)
    log(job, f"ingest done: {len(st['documents'])} document(s)")
    print(f"\njob dir: {job}\noutput dir: {out}")
    return job


def _runtime_master(job: Path, out: Path, st: dict) -> dict:
    return {
        "JOB_ID": st["job"],
        "PLAYGROUND": str(job),
        "OUTPUT": str(out),
        "INPUT (read-only)": str(INPUT),
        "SPECS": str(SPECS),
        "INGEST": str(job / "ingest"),
        "PROBLEMS_JSON": str(job / "problems.json"),
        "FINAL_DIR": str(out / "final"),
        "VALIDATOR_DIR": str(job / "validator"),
        "MAX_MASTER_ROUNDS": CONFIG["max_master_rounds"],
        "MAX_WORKER_ROUNDS": CONFIG["max_worker_rounds"],
        "fw command": "/home/xing/project/auto_hw_complete/framework/fw",
        "specs.md contents": "\n\n```\n" + (SPECS.read_text() if SPECS.exists()
                                            else "(none)") + "\n```",
    }


def cmd_run(args):
    job = cmd_init(args)
    _launch_master(job, first=True)


def cmd_resume(args):
    """Continue a job that was interrupted.

    Clears any problem left marked `running` by a killed process -- otherwise
    `fw spawn-worker` refuses forever on the strength of a stale flag.
    """
    job = find_job()
    st = load_state(job)
    stale = [p for p, v in st["problems"].items() if v["status"] == "running"]
    for pid in stale:
        st["problems"][pid]["status"] = "interrupted"
    if stale:
        save_state(job, st)
        log(job, f"resume: cleared stale running flag on {', '.join(stale)}")
    log(job, f"resuming job {st['job']}")
    _launch_master(job, first=False, stale=stale)


def _launch_master(job: Path, first: bool, stale=()):
    st = load_state(job)
    out = Path(st["output"])
    cfg = sandbox.make_config_dir(job)

    sp = system_prompt("master", "master", _runtime_master(job, out, st))
    if first:
        prompt = (
            "You are starting this homework run. Read the assignment through all "
            "three channels, cut it into problems, write problems.json, then run the "
            "workers one at a time with `fw spawn-worker <pid>`, assemble and compile "
            "the final answer document, and submit it with `fw submit`. Keep going "
            "until the master validator returns PASS or you exhaust "
            "MAX_MASTER_ROUNDS. Log your decisions as you go."
        )
    else:
        done = [p for p, v in st["problems"].items() if v["status"] == "done"]
        esc = [p for p, v in st["problems"].items() if v["status"] == "escalated"]
        prompt = (
            "This run was interrupted and has been resumed. Do not start over. "
            f"Read {job}/state.json, {job}/problems.json and {job}/logs/run.log to "
            "re-establish where you were, and check what is already on disk before "
            "redoing anything.\n"
            f"- finished problems: {', '.join(done) or 'none'}\n"
            f"- escalated problems: {', '.join(esc) or 'none'}\n"
            f"- problems interrupted mid-run (their work may be partial and must be "
            f"checked or respawned): {', '.join(stale) or 'none'}\n"
            f"- master submissions already used: {st['master_rounds']}/"
            f"{CONFIG['max_master_rounds']}\n"
            "Continue from there."
        )
    sid = st.get("master_session")
    resume = bool(sid)
    if not sid:
        sid = sandbox.new_session_id()
        st["master_session"] = sid
    st["status"] = "master_running"
    save_state(job, st)
    log(job, "spawning master agent" + (" (resumed)" if resume else ""))
    with Heartbeat(job, "master", CONFIG["heartbeat_seconds"]):
        rc, result, data = sandbox.run_agent(
            prompt=prompt, system_prompt=sp,
            rw_paths=[job, out], cfg_dir=cfg, chdir=job,
            model=CONFIG["model"], effort=CONFIG["effort"],
            log_path=job / "logs" / "master.json",
            session_id=sid, resume=resume,
            timeout=CONFIG["agent_timeout_seconds"],
            pip_cache=job / ".pipcache",
            pidfile=job / "logs" / "master.pid")
    record_cost(job, data, "master")
    st = load_state(job)
    st["status"] = "master_finished" if rc == 0 else f"master_failed_rc{rc}"
    save_state(job, st)
    log(job, f"master finished rc={rc}")
    print("\n" + "=" * 70 + "\nMASTER REPORT\n" + "=" * 70 + "\n" + result)


def _worker_dirs(job: Path, out: Path, pid: str):
    wpg = job / "problems" / pid
    wout = out / pid
    vdir = job / "validators" / pid
    for d in (wpg, wout, vdir):
        d.mkdir(parents=True, exist_ok=True)
    return wpg, wout, vdir


def cmd_spawn_worker(args):
    job = find_job()
    st = load_state(job)
    out = Path(st["output"])
    pid = args.pid

    running = [p for p, v in st["problems"].items()
               if v["status"] == "running" and p != pid]
    if running:
        sys.exit(f"REFUSED: problem {running[0]} is still running. "
                 "Workers run one at a time.")
    cur = st["problems"].get(pid)
    if cur and cur["status"] == "done" and not args.force:
        sys.exit(f"REFUSED: {pid} is already done. Use `fw respawn-worker {pid}`.")
    if cur and cur["status"] == "interrupted" and not args.force:
        sys.exit(f"{pid} was interrupted mid-run and its work may be partial. "
                 f"Either `fw respawn-worker {pid}` to start it clean, or "
                 f"`fw spawn-worker {pid} --force` to continue from what is there.")

    wpg, wout, vdir = _worker_dirs(job, out, pid)
    dl = wpg / "downloads.md"
    if not dl.is_file():
        # Pre-created so "I installed nothing" is an explicit statement rather than a
        # missing file the validator has to interpret (rule R3).
        dl.write_text("# Downloads and installs for this problem\n\n"
                      "One line per item: `- <name> | <how> | <path> | <why>`\n"
                      "If you install nothing, write `- (nothing installed)`.\n\n")
    brief = wpg / "problem.md"
    if not brief.is_file():
        sys.exit(f"REFUSED: {brief} does not exist. Write the problem brief first.")

    st["problems"][pid] = {"status": "running", "rounds": 0, "started": now()}
    if pid not in st["problem_order"]:
        st["problem_order"].append(pid)
    save_state(job, st)

    runtime_w = {
        "PROBLEM_ID": pid, "PLAYGROUND": str(wpg), "OUTPUT": str(wout),
        "problem.md": str(brief), "INGEST": str(job / "ingest"),
        "INPUT (read-only)": str(INPUT),
        "MAX_ROUNDS": CONFIG["max_worker_rounds"],
    }
    runtime_v = dict(runtime_w)
    runtime_v.update({
        "VALIDATOR_DIR (your only writable dir)": str(vdir),
        "CHECKLIST": str(vdir / "checklist.md"),
        "WORKER_PLAYGROUND (read-only to you)": str(wpg),
        "WORKER_OUTPUT (read-only to you)": str(wout),
        "note": ("You cannot write into the worker's directories. To re-run one of "
                 "its scripts, copy the script into your own dir and run it there."),
    })
    sp_w = system_prompt("worker", "worker", runtime_w)
    sp_v = system_prompt("worker_validator", "worker", runtime_v)

    wsid = sandbox.new_session_id()
    vsid = sandbox.new_session_id()
    wcfg = sandbox.make_config_dir(wpg)
    vcfg = sandbox.make_config_dir(vdir)
    feedback = None
    verdict = "FAIL"

    for rnd in range(1, CONFIG["max_worker_rounds"] + 1):
        log(job, f"{pid}: worker round {rnd}")
        if rnd == 1:
            wprompt = (f"Solve the problem described in {brief}. Work in your "
                       f"PLAYGROUND, deliver to your OUTPUT, and write "
                       f"PLAYGROUND/submission.md when you are done.")
        else:
            wprompt = ("Your validator rejected the submission. Fix these defects, "
                       "then update PLAYGROUND/submission.md.\n\n"
                       f"{feedback}")
        with Heartbeat(job, f"{pid} worker round {rnd}", CONFIG["heartbeat_seconds"]):
            rc, wres, wdata = sandbox.run_agent(
                prompt=wprompt, system_prompt=sp_w,
                rw_paths=[wpg, wout], cfg_dir=wcfg, chdir=wpg,
                model=CONFIG["model"], effort=CONFIG["effort"],
                log_path=job / "logs" / f"{pid}_worker_r{rnd}.json",
                session_id=wsid, resume=(rnd > 1),
                timeout=CONFIG["agent_timeout_seconds"],
                pip_cache=wpg / ".pipcache",
                pidfile=job / "logs" / "current_agent.pid")
        record_cost(job, wdata, f"{pid} worker r{rnd}")
        log(job, f"{pid}: worker round {rnd} rc={rc}")
        if rc == 124:
            log(job, f"{pid}: worker round {rnd} TIMED OUT")

        vprompt = (f"Audit round {rnd} of the worker's attempt at the problem in "
                   f"{brief}. Its submission pointer is {wpg}/submission.md. "
                   "Assume it is wrong and go find out where. End with VERDICT: PASS "
                   "or VERDICT: FAIL.")
        with Heartbeat(job, f"{pid} validator round {rnd}",
                       CONFIG["heartbeat_seconds"]):
            rc, vres, vdata = sandbox.run_agent(
                prompt=vprompt, system_prompt=sp_v,
                rw_paths=[vdir], cfg_dir=vcfg, chdir=vdir,
                model=CONFIG["model"], effort=CONFIG["effort"],
                log_path=job / "logs" / f"{pid}_validator_r{rnd}.json",
                session_id=vsid, resume=(rnd > 1),
                timeout=CONFIG["agent_timeout_seconds"],
                pip_cache=vdir / ".pipcache",
                pidfile=job / "logs" / "current_agent.pid")
        record_cost(job, vdata, f"{pid} validator r{rnd}")

        verdict = classify(rc, vres, vdata)
        if verdict == "ERROR":
            log(job, f"{pid}: validator round {rnd} ERRORED -- fresh session, retry")
            vsid = sandbox.new_session_id()
            with Heartbeat(job, f"{pid} validator r{rnd} retry",
                           CONFIG["heartbeat_seconds"]):
                rc, vres, vdata = sandbox.run_agent(
                    prompt=vprompt, system_prompt=sp_v,
                    rw_paths=[vdir], cfg_dir=vcfg, chdir=vdir,
                    model=CONFIG["model"], effort=CONFIG["effort"],
                    log_path=job / "logs" / f"{pid}_validator_r{rnd}_retry.json",
                    session_id=vsid, resume=False,
                    timeout=CONFIG["agent_timeout_seconds"],
                    pip_cache=vdir / ".pipcache",
                    pidfile=job / "logs" / "current_agent.pid")
            record_cost(job, vdata, f"{pid} validator r{rnd} retry")
            verdict = classify(rc, vres, vdata)
            if verdict == "ERROR":
                verdict = "FAIL"   # two harness failures: stop, do not loop forever
        log(job, f"{pid}: validator round {rnd} -> {verdict}")
        st = load_state(job)
        st["problems"][pid]["rounds"] = rnd
        save_state(job, st)
        if verdict == "PASS":
            break
        feedback = vres

    st = load_state(job)
    st["problems"][pid]["status"] = "done" if verdict == "PASS" else "escalated"
    st["problems"][pid]["finished"] = now()
    save_state(job, st)

    if verdict == "PASS":
        print(f"\n{pid}: DONE after {st['problems'][pid]['rounds']} round(s).")
        print(f"deliverable: {wout}")
    else:
        print(f"\n{pid}: ESCALATED -- the validator did not pass it within "
              f"{CONFIG['max_worker_rounds']} rounds.")
        print(f"read {vdir/'checklist.md'} and decide what to do.")
        print("\n--- last validator feedback ---\n" + (feedback or "")[:4000])


def cmd_respawn_worker(args):
    job = find_job()
    st = load_state(job)
    out = Path(st["output"])
    pid = args.pid
    wpg, wout, vdir = _worker_dirs(job, out, pid)
    brief = wpg / "problem.md"
    keep = brief.read_text() if brief.is_file() else None
    archive = job / "archive" / f"{pid}_{dt.datetime.now():%H%M%S}"
    archive.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(wpg), str(archive))
    if wout.exists():
        shutil.rmtree(wout)
    wpg, wout, vdir = _worker_dirs(job, out, pid)
    if keep:
        brief.write_text(keep)
    st["problems"].pop(pid, None)
    save_state(job, st)
    log(job, f"{pid}: respawned (old work archived to {archive})")
    args.force = True
    cmd_spawn_worker(args)


def cmd_submit(args):
    job = find_job()
    st = load_state(job)
    out = Path(st["output"])
    if st["master_rounds"] >= CONFIG["max_master_rounds"]:
        sys.exit(f"REFUSED: MAX_MASTER_ROUNDS ({CONFIG['max_master_rounds']}) "
                 "already used. Stop and report what is unresolved.")
    unfinished = [p for p, v in st["problems"].items() if v["status"] == "running"]
    if unfinished:
        sys.exit(f"REFUSED: {unfinished[0]} is still running.")

    st["master_rounds"] += 1
    rnd = st["master_rounds"]
    save_state(job, st)
    vdir = job / "validator"
    vdir.mkdir(parents=True, exist_ok=True)

    runtime = _runtime_master(job, out, st)
    runtime.update({
        "VALIDATOR_DIR (your only writable dir)": str(vdir),
        "CHECKLIST": str(vdir / "checklist.md"),
        "SUBMISSION_ROUND": rnd,
        "note": ("The master's playground and output are read-only to you. Copy "
                 "anything you want to re-run into your own dir."),
    })
    sp = system_prompt("master_validator", "master", runtime)
    sid_file = vdir / ".session_id"
    if sid_file.is_file():
        sid, resume = sid_file.read_text().strip(), True
    else:
        sid, resume = sandbox.new_session_id(), False
        sid_file.write_text(sid)

    log(job, f"submitting to master validator (round {rnd})")
    for attempt in (1, 2):
      with Heartbeat(job, f"master validator round {rnd}", CONFIG["heartbeat_seconds"]):
        rc, res, vdata = sandbox.run_agent(
        prompt=(f"Submission round {rnd}. The master claims the job is finished. "
                f"The assembled answer is in {out/'final'}. Validate it and append "
                f"round {rnd} to your checklist. End with VERDICT: PASS or "
                f"VERDICT: FAIL."),
        system_prompt=sp,
        rw_paths=[vdir], cfg_dir=sandbox.make_config_dir(vdir), chdir=vdir,
        model=CONFIG["model"], effort=CONFIG["effort"],
        log_path=job / "logs" / f"master_validator_r{rnd}.json",
        session_id=sid, resume=resume,
        timeout=CONFIG["agent_timeout_seconds"], pip_cache=vdir / ".pipcache",
        pidfile=job / "logs" / "current_agent.pid")
      record_cost(job, vdata, f"master validator r{rnd}")
      outcome = classify(rc, res, vdata)
      if outcome != "ERROR" or attempt == 2:
          break
      # The validator reads every page of the PDF as an image (rule R7), so a resumed
      # session accumulates them and eventually trips the API's many-image limit.
      # The checklist on disk is the durable memory, so a fresh session loses nothing
      # that matters -- "norefresh" degrades to "the notes persist".
      log(job, f"master validator r{rnd} ERRORED ({(res or '')[:120]!r}); "
               "retrying once with a fresh session")
      sid, resume = sandbox.new_session_id(), False
      sid_file.write_text(sid)

    if outcome == "ERROR":
        st = load_state(job)
        st["master_rounds"] = max(0, st["master_rounds"] - 1)   # not a real round
        st["status"] = "validator_error"
        save_state(job, st)
        log(job, f"master validator round {rnd} ERRORED twice -- round refunded")
        print("=" * 70)
        print("THE VALIDATOR FAILED TO RUN. This is a harness error, not a verdict.\n")
        print((res or "")[:1000])
        print("\nThe submission was NOT judged. Do not treat this as feedback and do "
              "not 'fix' anything on the strength of it. Try `fw submit` again.")
        return

    passed = outcome == "PASS"
    st = load_state(job)
    st["status"] = "passed" if passed else "needs_rework"
    save_state(job, st)
    log(job, f"master validator round {rnd} -> {outcome}")
    print("=" * 70)
    print(res)
    print("=" * 70)
    if passed:
        print(f"\nPASS. The job is done. Final answer: {out/'final'}")
    else:
        remaining = CONFIG["max_master_rounds"] - rnd
        print(f"\nFAIL. Fix the defects above and submit again. "
              f"{remaining} submission(s) remaining.")


def cmd_despawn(args):
    """Kill the agent currently running, from another terminal.

    bwrap runs with --die-with-parent, so killing the sandbox takes the agent with it.
    We use a pidfile rather than `pkill -f claude`, which would also match the caller.
    """
    job = find_job()
    pidfile = job / "logs" / "current_agent.pid"
    if args.master or not pidfile.is_file():
        pidfile = job / "logs" / "master.pid"
    if not pidfile.is_file():
        sys.exit("no agent is currently running")
    pid = int(pidfile.read_text().strip())
    try:
        os.kill(pid, signal.SIGTERM)
        log(job, f"despawned agent pid {pid}")
        print(f"sent SIGTERM to {pid}. Run `fw resume` to pick the job back up.")
    except ProcessLookupError:
        pidfile.unlink(missing_ok=True)
        sys.exit(f"pid {pid} is not running (stale pidfile removed)")


def cmd_status(args):
    job = find_job()
    st = load_state(job)
    print(f"job:     {st['job']}  ({st['status']})")
    print(f"created: {st['created']}")
    print(f"master submissions used: {st['master_rounds']}/"
          f"{CONFIG['max_master_rounds']}")
    print(f"cost so far: ${st.get('cost_usd', 0.0):.2f}")
    hb = job / "logs" / "heartbeat.log"
    if hb.is_file():
        last = hb.read_text().strip().splitlines()
        if last:
            print(f"last heartbeat: {last[-1]}")
    if not st["problems"]:
        print("no problems spawned yet")
        return
    print("\nproblems:")
    for pid in st.get("problem_order", list(st["problems"])):
        v = st["problems"][pid]
        print(f"  {pid:8s} {v['status']:10s} rounds={v.get('rounds', 0)}"
              f"/{CONFIG['max_worker_rounds']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    pi = sub.add_parser("init")
    pi.add_argument("--fresh", action="store_true")
    pr = sub.add_parser("run")
    pr.add_argument("--fresh", action="store_true")
    sub.add_parser("resume")
    sub.add_parser("status")
    sub.add_parser("submit")
    pd = sub.add_parser("despawn")
    pd.add_argument("--master", action="store_true")
    for name in ("spawn-worker", "respawn-worker"):
        p = sub.add_parser(name)
        p.add_argument("pid")
        p.add_argument("--force", action="store_true")
    a = ap.parse_args()
    {"init": cmd_init, "run": cmd_run, "resume": cmd_resume, "status": cmd_status,
     "submit": cmd_submit, "despawn": cmd_despawn,
     "spawn-worker": cmd_spawn_worker,
     "respawn-worker": cmd_respawn_worker}[a.cmd](a)


if __name__ == "__main__":
    main()
