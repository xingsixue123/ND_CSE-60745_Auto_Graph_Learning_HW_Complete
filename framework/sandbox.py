"""Hard sandbox for agent processes.

Wraps `claude -p` in bubblewrap so that the ONLY writable paths are the ones we
bind explicitly.  Everything else on the machine -- including input/, framework/,
$HOME and the system -- becomes a read-only filesystem at the kernel level.

Why not Claude Code's built-in `sandbox` setting?  Verified on this machine:

  * `--permission-mode bypassPermissions` silently disables it, so you cannot have
    both prompt-free operation and enforcement;
  * its network layer is an allowlist-only egress proxy with no wildcard
    (`allowedDomains: ["*"]` still 403s everything), so workers could not download;
  * it does not nest -- a sandboxed agent cannot spawn a working child agent
    (the child inherits the parent mount namespace and dies with
    `EROFS ... mkdir ~/.claude/session-env/<uuid>`).

bwrap has none of those problems: it nests correctly (an inner sandbox is strictly
tighter than its parent), leaves the network alone, and lets us pass
--dangerously-skip-permissions safely because the kernel, not the model, is the
thing saying no.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import uuid
from pathlib import Path

HOME = Path.home()
REAL_CREDENTIALS = HOME / ".claude" / ".credentials.json"


def _require_bwrap() -> str:
    bw = shutil.which("bwrap")
    if not bw:
        raise RuntimeError("bubblewrap (bwrap) not found; the sandbox cannot be enforced")
    return bw


def make_config_dir(base: Path) -> Path:
    """A private CLAUDE_CONFIG_DIR so agents never touch the real ~/.claude.

    The real credentials file is bind-mounted in read-only rather than copied, so no
    copy of the token is ever written into a playground.
    """
    cfg = base / ".claudecfg"
    cfg.mkdir(parents=True, exist_ok=True)
    (cfg / ".credentials.json").touch(exist_ok=True)
    return cfg


def bwrap_prefix(rw_paths, cfg_dir: Path, chdir: Path, pip_cache: Path | None = None):
    """Build the bwrap argv prefix.

    rw_paths -- directories that become writable.  Everything else is read-only.
    """
    bw = _require_bwrap()
    argv = [
        bw,
        "--ro-bind", "/", "/",
        "--dev", "/dev",
        "--proc", "/proc",
        "--tmpfs", "/tmp",
    ]
    for p in rw_paths:
        p = Path(p).resolve()
        p.mkdir(parents=True, exist_ok=True)
        argv += ["--bind", str(p), str(p)]

    cfg_dir = Path(cfg_dir).resolve()
    argv += ["--bind", str(cfg_dir), str(cfg_dir)]
    if REAL_CREDENTIALS.exists():
        # ro-bind *after* the cfg bind so it layers on top
        argv += ["--ro-bind", str(REAL_CREDENTIALS), str(cfg_dir / ".credentials.json")]

    argv += [
        "--setenv", "CLAUDE_CONFIG_DIR", str(cfg_dir),
        "--setenv", "HOME", str(HOME),
        "--setenv", "PATH", os.environ.get("PATH", "/usr/bin:/bin"),
    ]
    if pip_cache:
        pip_cache = Path(pip_cache).resolve()
        argv += ["--setenv", "PIP_CACHE_DIR", str(pip_cache)]

    argv += [
        "--chdir", str(Path(chdir).resolve()),
        "--die-with-parent",
        "--unshare-pid",
    ]
    return argv


def new_session_id() -> str:
    return str(uuid.uuid4())


def run_agent(*, prompt: str, system_prompt: str, rw_paths, cfg_dir: Path,
              chdir: Path, model: str, effort: str, log_path: Path,
              session_id: str | None = None, resume: bool = False,
              timeout: int = 7200, pip_cache: Path | None = None,
              pidfile: Path | None = None):
    """Spawn one sandboxed agent, blocking until it finishes.

    Writes the sandbox pid to `pidfile` while it runs so an operator in another
    terminal can kill a hung agent (bwrap is started with --die-with-parent, so
    killing it takes the agent down with it).

    Returns (returncode, result_text, raw_json_or_none).
    """
    import json

    chdir = Path(chdir)
    chdir.mkdir(parents=True, exist_ok=True)
    sysfile = Path(cfg_dir) / "system_prompt.md"
    sysfile.parent.mkdir(parents=True, exist_ok=True)
    sysfile.write_text(system_prompt)

    argv = bwrap_prefix(rw_paths, cfg_dir, chdir, pip_cache=pip_cache)
    # --append-system-prompt-file is undocumented in --help but works, and keeps
    # multi-KB system prompts out of argv (where they would also be visible to
    # `pkill -f` style matches).
    argv += [
        "claude", "-p", prompt,
        "--model", model,
        "--settings", f'{{"effortLevel":"{effort}"}}',
        "--append-system-prompt-file", str(sysfile),
        "--dangerously-skip-permissions",
        "--output-format", "json",
    ]
    if session_id and resume:
        argv += ["--resume", session_id]
    elif session_id:
        argv += ["--session-id", session_id]

    log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    proc = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            stdin=subprocess.DEVNULL, text=True)
    if pidfile:
        Path(pidfile).write_text(str(proc.pid))
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.communicate()
        log_path.write_text("TIMEOUT after %ds\n" % timeout)
        return 124, f"AGENT TIMED OUT after {timeout}s with no result.", None
    finally:
        if pidfile and Path(pidfile).exists():
            Path(pidfile).unlink()

    log_path.write_text(out + ("\n--- stderr ---\n" + err if err else ""))
    try:
        data = json.loads(out)
        return proc.returncode, data.get("result", ""), data
    except Exception:
        return proc.returncode, out, None
