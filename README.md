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

## Requirements

Linux with `bwrap` and `socat`, the `claude` CLI, a TeX installation, LibreOffice
for Office-format inputs, and `pymupdf`. `framework/env.md` records exactly what
was verified present, and — more usefully — what is absent, so no agent wastes a
round rediscovering it.
