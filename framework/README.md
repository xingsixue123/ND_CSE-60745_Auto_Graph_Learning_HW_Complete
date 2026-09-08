# auto_hw_complete

A homework assignment goes into `input/`; a compiled PDF of answers comes out of
`output/<job>/final/`. Four kinds of agent do the work, each in a hard sandbox.

## Running it

    # 1. put the assignment (and its data) in input/, and describe it in specs.md
    # 2.
    framework/fw run

That ingests the input, spawns the master agent, and blocks until the master
validator passes the work or the submission cap is hit.

    framework/fw status      where the job is, cost so far, last heartbeat
    framework/fw resume      continue a job that was interrupted
    framework/fw despawn     kill the agent currently running (from another terminal)
    framework/fw init        ingest only, spawn nothing
    framework/fw run --fresh throw an existing job away and start it over

`fw run` refuses to clobber an existing job: the job id is deterministic in the input
and the date, so re-running it would otherwise land on the same directory and wipe
every finished problem. Use `fw resume` — the master is handed back its own session
plus a summary of what is finished, escalated, or interrupted, and told not to start
over. Any problem left flagged `running` by a killed process is cleared to
`interrupted` so it cannot block the queue forever.

Progress goes to `playground/<job>/logs/run.log`. Because `fw spawn-worker` blocks the
master for the whole duration of a problem, the master cannot log its own status on a
timer — the driver does it instead, appending a heartbeat every `heartbeat_seconds`
(default 10 min) naming the phase and elapsed wall-clock.

## The agents

| agent | count | writable dirs | job |
|---|---|---|---|
| master | 1 | `playground/<job>/`, `output/<job>/` | cut the assignment into problems, run the workers, assemble and compile the answer, submit |
| master validator | 1, persistent | `playground/<job>/validator/` | audit the whole submission; keeps a checklist across rounds |
| worker | 1 per problem | `playground/<job>/problems/<pid>/`, `output/<job>/<pid>/` | solve one problem, deliver a LaTeX fragment (+ figures) |
| worker validator | 1 per problem, persistent | `playground/<job>/validators/<pid>/` | audit that worker; keeps a checklist across rounds |

Master and master validator receive byte-identical `env.md` + `rules.md` +
`context_master.md`; worker and worker validator receive identical `env.md` +
`rules.md` + `context_worker.md`. Only the role section and the runtime paths differ.
A validator that knows less than the agent it audits cannot audit it.

Workers run strictly one at a time — `fw spawn-worker` refuses to start a second
problem while one is unfinished.

## The sandbox

Every agent runs under `bwrap`. The **only** writable paths are the ones in the table
above; the rest of the machine — `input/`, `framework/`, `$HOME`, the system — is a
read-only filesystem, enforced by the kernel. Agents run with
`--dangerously-skip-permissions` inside, which is safe precisely because the sandbox,
not the model, is the thing saying no. Network is unrestricted.

Claude Code's own `sandbox` setting is deliberately **not** used. Verified on this
machine: `bypassPermissions` silently disables it; its egress allowlist has no
wildcard so workers could not download anything; and it does not nest, so a sandboxed
master cannot spawn a working child (`EROFS ... ~/.claude/session-env`). bwrap nests
correctly — an inner sandbox is strictly tighter than its parent — which is what makes
"master spawns its own workers" possible at all.

Each agent gets a private `CLAUDE_CONFIG_DIR`; the real credentials file is
bind-mounted read-only rather than copied, so no token is ever written into a
playground.

## Termination

Nothing loops forever. A worker gets `max_worker_rounds` (default 5) attempts with its
validator; if the validator still refuses, the problem comes back **ESCALATED** and the
master decides what to do. The master gets `max_master_rounds` (default 5) submissions
to the master validator. Both caps are in `config.json` and are enforced in `fw.py`,
not in a prompt.

## Files

    framework/
      fw, fw.py          driver: init / run / status / spawn-worker / respawn-worker / submit
      sandbox.py         bwrap wrapper; the only thing that decides what is writable
      ingest.py          input/ -> per-page PNGs + text (LibreOffice for Office formats)
      config.json        model, effort, round caps, timeouts
      env.md             what this machine can and cannot do — given to every agent
      rules.md           the hard rules — given to every agent
      prompts/
        context_master.md      shared by master + master validator
        context_worker.md      shared by worker + worker validator
        master.md master_validator.md worker.md worker_validator.md
      tools/
        pdf_pages.py     dual-channel PDF reader (image + text)
        lint_output.py   enforces "OUTPUT is a deliverable, not a workspace"
        cleanup.py       remove a job's artifacts and installed packages

## Cleaning up

    python3 framework/tools/cleanup.py --list
    python3 framework/tools/cleanup.py <job_id>

Workers record every install in their `downloads.md` (rule R3), and everything they
install lives inside their playground, so removing the job directory removes it all.

## Reading the assignment — three channels

`ingest.py` produces, per page: the extracted **text**, a 200 dpi **page render**, and
every embedded **figure at its native resolution**. All three are needed, because each
fails differently and none of the failures announce themselves:

- text silently omits every figure;
- the page render carries figures but is downscaled when an agent reads it, so small
  labels inside a figure become unreadable — you see *that* there is a graph, not what
  it says;
- the figure files are the only channel that reliably carries figure content.

Measured on this assignment: an agent asked to transcribe the Q1 graph got the correct
15-edge, 3-regular answer **only** by locating the node disks and testing all 45
candidate pairs for ink. Reading it by eye — including by a careful human reader —
produced a wrong answer, because a line passing *behind* a node looks exactly like two
lines meeting *at* it. `context_worker.md` carries that method, and requires a global
invariant check (degree sum = 2|E|) before a transcription is trusted.

## Environment notes

See `framework/env.md` — the verified capability sheet for this machine, handed to
every agent. Short version: LaTeX works (TinyTeX, but `tlmgr install` does not work
from inside the sandbox, so the package set is fixed); poppler and LibreOffice are
installed root-free in `~/local` and `~/miniconda3/envs/sandbox_tools`; `pip` must go
into a venv inside the playground and `conda create` does not work at all, because
`~/miniconda3` is read-only to agents.
