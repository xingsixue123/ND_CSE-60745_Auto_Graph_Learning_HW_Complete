# HARD RULES

These are not guidelines. The first three are enforced by the kernel — you will get
`Read-only file system` errors rather than a refusal, and no amount of retrying,
`sudo`, or creative pathing will change that. The rest are enforced by the harness,
which will reject your work and make you redo it.

## R1 — Filesystem

You may write **only** inside the directories listed in your prompt as
`PLAYGROUND` and `OUTPUT`. Everything else on this machine, including
`input/`, `framework/`, other agents' directories, `$HOME`, and the system, is
mounted read-only.

`input/` is readable but never writable. Never attempt to modify, move, rename or
"clean up" the user's input files.

## R2 — No escaping

Do not attempt to widen your sandbox: no editing of settings files, no re-invoking
yourself or any other agent with different sandbox flags, no writing to another
agent's directory. If you believe you genuinely need write access somewhere else,
stop and say so in your report instead of working around it.

## R3 — Downloads must be recorded

You may install and download whatever you need (see `env.md`). Everything you install
must go inside your PLAYGROUND (a venv, a cloned repo, a downloaded dataset), and
every install must be appended to `PLAYGROUND/downloads.md` with one line per item:

    - <name> | <how it was installed> | <path> | <why>

This file is what lets the run be cleaned up later. An install you did not record is
a defect and the validator will send it back.

## R4 — OUTPUT is a clean deliverable, not a workspace

`OUTPUT` may contain only:

  - `answer.tex`        — required
  - `preamble.txt`      — optional
  - `fig_*.pdf`         — optional, any number
  - `assets/`           — optional, only if a figure genuinely needs data files

No code, no logs, no `.aux`/`.log`/`.out`, no notebooks, no venvs, no intermediate
CSVs, no scratch images. All of that lives in PLAYGROUND. Run
`python3 framework/tools/lint_output.py <OUTPUT>` before you declare yourself done;
it exits non-zero and names the offenders.

## R5 — answer.tex is a FRAGMENT

`answer.tex` must **not** contain `\documentclass`, `\begin{document}`,
`\end{document}`, or `\usepackage`. It is `\input{}` into a larger document by the
master agent. It starts at the section level.

Extra packages you need go one-per-line in `preamble.txt` as literal `\usepackage{...}`
lines. The master merges and de-duplicates them.

**Every label, figure file and macro you define must be namespaced with your problem
id**, e.g. for problem `p3`:

    \label{p3:eq:flow}          not  \label{eq:flow}
    \includegraphics{fig_p3_degree.pdf}   not  \includegraphics{fig1.pdf}

Unnamespaced labels collide across problems and break the master's compile. This is
the single most common way this pipeline fails.

Reference figures by **bare filename** (`fig_p3_degree.pdf`), never by absolute path —
the master copies them next to the assembled document.

## R6 — Termination is decided by your validator, not by you

You do not get to declare yourself finished. You submit; your validator decides.
The loop is capped (see `MAX_ROUNDS` in your prompt). If you hit the cap without the
validator passing you, the harness escalates — it does not silently accept the work.

## R7 — Read every PDF through all three channels

Whenever you read a homework PDF you must use **all three** channels and reconcile
them (see `env.md` for the mechanics):

  1. the extracted **text** (`page_00N.txt`),
  2. the rendered **page image** (`page_00N.png`),
  3. the **extracted figure files** (`page_00N_fig_NN.*`), at native resolution.

This is not ceremony. Text extraction drops every figure without erroring. The
whole-page image gets downscaled when you read it, so small labels inside a figure
become unreadable — you will see that a figure exists and not what it contains. The
figure files are the only channel that reliably carries figure content.

**Any figure a question refers to must be read from its figure file**, and if it is
still too small, cropped and upscaled before you read it. A claim that rests on a
figure you could not actually read is a guess; say so rather than asserting it.

A claim that appears in only one channel is unverified. Where channels disagree, say
which one you trusted and why.
