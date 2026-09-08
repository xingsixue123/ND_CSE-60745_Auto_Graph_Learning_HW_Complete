# auto_hw_complete

A homework assignment goes into `input/`. A compiled PDF of answers comes out of
`output/<job>/final/`. Four kinds of agent do the work, each confined to its own
kernel-enforced sandbox.

The point of interest is not that agents can answer homework questions — it is
what has to be true for the answers to be trustworthy: that no agent can write
outside its own directory, that nothing declares itself finished, that a figure
is never read by squinting at it, and that the loop always terminates.

```bash
# put the assignment and its data in input/, describe it in specs.md
framework/fw run
```

`examples/` holds one complete run: a legacy `.doc`, a 26k-edge graph file, a
**three-line** `specs.md` — and the 10-page answer PDF that came out, together
with the full trajectory that produced it.

## The agents

| agent | count | writable dirs | job |
|---|---|---|---|
| master | 1 | `playground/<job>/`, `output/<job>/` | cut the assignment into problems, run the workers, assemble and compile the answer, submit |
| master validator | 1, persistent | `playground/<job>/validator/` | audit the whole submission; keeps a checklist across rounds |
| worker | 1 per problem | `playground/<job>/problems/<pid>/`, `output/<job>/<pid>/` | solve one problem, deliver a LaTeX fragment and figures |
| worker validator | 1 per problem, persistent | `playground/<job>/validators/<pid>/` | audit that worker, starting from the assumption it is wrong |

Master and master validator receive byte-identical background (`env.md` +
`rules.md` + `context_master.md`); worker and worker validator likewise share
`context_worker.md`. Only the role section and the runtime paths differ. A
validator that knows less than the agent it audits cannot audit it.

Workers run strictly one at a time — the driver refuses to start a second
problem while one is unfinished.

## The sandbox

Every agent runs under its own `bwrap` sandbox. The **only** writable paths are
the ones in the table above; `input/`, `framework/`, `$HOME` and the rest of the
machine are a read-only filesystem, enforced by the kernel rather than by asking
the model nicely. Credentials are bind-mounted read-only, so no token is ever
written to disk.

Claude Code's own `sandbox` setting is deliberately not used. Measured on the
target machine: `bypassPermissions` silently disables it, so you cannot have both
prompt-free operation and enforcement; its egress layer is an allowlist-only
proxy with no wildcard, so workers could not install anything; and it does not
nest — a sandboxed master cannot spawn a working child agent. `bwrap` has none of
those problems, and it nests correctly, which is what makes "the master spawns
its own workers" possible at all.

## Reading the assignment

Three channels, because each is lossy in a different way and none of the failures
announce themselves:

1. **extracted text** silently omits every figure — a question saying "create the
   following graph" leaves a blank gap, not an error;
2. **the rendered page** carries figures but is downscaled when an agent reads
   it, so small labels inside a figure become unreadable — you can see *that*
   there is a graph, not what it says;
3. **figures extracted at native resolution** are the only channel that reliably
   carries figure content.

Even then, transcribing a drawing into data is done by **measurement, not by
looking**. A line passing behind a node is visually indistinguishable from two
lines meeting at it, at any magnification — it is geometric ambiguity, not a
resolution problem. Workers locate the marks programmatically, test every
candidate relation for ink, and confirm against a global invariant before the
transcription is trusted.

## Termination

Nothing loops forever and nothing declares itself finished. A worker gets
`max_worker_rounds` attempts with its validator; if the validator still refuses,
the problem returns **escalated** and the master decides. The master gets
`max_master_rounds` submissions. Both caps live in `config.json` and are enforced
in code, not in a prompt.

A validator that *crashes* is distinguished from one that returns a verdict: a
harness error is never fed back to the master as if it were a defect list, and it
does not consume a round.

## Layout

```
input/          the assignment and its data      (read-only to every agent)
specs.md        anything else the master should know
output/<job>/   deliverables; final/ is the answer document
playground/<job>/   scratch space, one directory per agent
framework/      the pipeline itself -- read-only to every agent
  fw, fw.py     driver: run / resume / status / spawn-worker / submit / despawn
  sandbox.py    the bwrap wrapper; the only thing that decides what is writable
  ingest.py     any input format -> per-page renders, text and native-res figures
  env.md        verified machine capability sheet, given to every agent
  rules.md      the hard rules, given to every agent
  prompts/      two shared context files + four role files
  tools/        pdf_pages, lint_output, crosscheck, cleanup
examples/       one complete worked run, input through deliverable
```

`framework/README.md` documents the pipeline in detail; `examples/README.md`
walks through the worked run.

## Setup

Only the first step needs root. Everything else installs into your home directory,
which is deliberate: the machine this was built on has no `sudo`.

**1. bubblewrap** — the sandbox. The one hard requirement.

```bash
sudo apt install bubblewrap            # Debian/Ubuntu
bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp true && echo ok
```

`socat` is *not* needed. Claude Code's built-in sandbox requires it, but this
pipeline never enables that sandbox — it wraps the agent in `bwrap` itself.

**2. The `claude` CLI, logged in.** No API key: credentials are read from
`~/.claude/.credentials.json` and bind-mounted **read-only** into each agent, so no
token is ever written into a playground. Run `claude` once interactively to log in.

**3. TeX.** TinyTeX or TeX Live. TinyTeX's default scheme is too small — it lacks
`listings`, `pgfplots`, `algorithmicx` and much else that homework answers reach
for. Agents **cannot** `tlmgr install` from inside the sandbox (`~/.TinyTeX` is
read-only to them), so the package set has to be complete up front:

```bash
tlmgr install amsmath amscls amsfonts tools graphics geometry booktabs \
  hyperref xcolor float enumitem siunitx pgf pgfplots caption algorithms \
  algorithmicx algorithm2e physics mathtools standalone adjustbox collectbox \
  wrapfig multirow fancyhdr titlesec microtype ulem cancel etoolbox xkeyval \
  environ trimspaces pdflscape threeparttable tcolorbox listings \
  listingsutf8 lastpage l3packages l3kernel soul upquote fvextra framed
tlmgr install ctex xecjk fandol zhnumber ctablestack   # only if you need CJK
```

`bm` and `longtable` are *not* separate packages — both ship inside `tools`, and
naming them makes `tlmgr` abort the whole batch. Verify by style file rather than
by package name: `kpsewhich bm.sty`.

**4. LibreOffice**, for `.doc` / `.docx` / `.pptx` inputs — extracted, not installed:

```bash
curl -LO https://download.documentfoundation.org/libreoffice/stable/26.2.6/deb/x86_64/LibreOffice_26.2.6_Linux_x86-64_deb.tar.gz
tar xzf LibreOffice_26.2.6_Linux_x86-64_deb.tar.gz
for d in LibreOffice_*/DEBS/*.deb; do dpkg-deb -x "$d" ~/local/libreoffice; done
ln -sf ~/local/libreoffice/opt/libreoffice26.2/program/soffice ~/.local/bin/soffice
```

**5. poppler**, so the `Read` tool can open a `.pdf` directly (without it, reading a
PDF fails outright with *"pdftoppm is not installed"*):

```bash
conda create -y -n sandbox_tools -c conda-forge poppler
# the conda binaries need their own env's libraries, so wrap rather than symlink
for b in pdftoppm pdftotext pdfinfo pdftocairo; do
  printf '#!/bin/bash
export LD_LIBRARY_PATH="%s/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
exec "%s/bin/%s" "$@"
'     "$HOME/miniconda3/envs/sandbox_tools" "$HOME/miniconda3/envs/sandbox_tools" "$b" > ~/.local/bin/$b
  chmod +x ~/.local/bin/$b
done
```

**6. Python.** `pymupdf` is required — it is the only PDF reader the tooling uses.
`matplotlib`, `numpy`, `scipy`, `pandas` and `networkx` are worth having; workers
can otherwise build their own venv inside their playground (`conda create` will not
work — `~/miniconda3` is read-only to them).

**7. Tell the agents the truth about your machine.** `framework/env.md` is handed
to every agent as ground truth and currently describes *this* machine — including
an absolute path to a Python environment with matplotlib. Update it to match yours.
Getting this file wrong is expensive: an agent will spend a whole round discovering
that something you claimed exists does not.

The pipeline itself is relocatable — clone it anywhere and `framework/fw` works
from any directory.

### Verifying

```bash
framework/fw init          # should refuse: input/ has no assignment in it
```

Then drop the worked example back in and run it:

```bash
cp examples/specs.md . && cp examples/input/* input/
framework/fw run
```
