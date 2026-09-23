# p4 — Ex. 2.5 (20 pts) + Ex. 2.6 (5 pts): pseudo-code for fork/exec/waitpid/exit, and zombies

**Problem id: `p4`.** Namespace every label, listing name and macro with `p4`
(e.g. `\label{p4:alg:fork}`).

## Where this lives in the assignment

The assignment is a **plain markdown file**, not a PDF or a Word document:

    /home/xing/project/auto_hw_complete/input/hw2_instruction.md

Ingest produced **no page PNGs and no figure files** for it — only
`ingest/pages/hw2_instruction/alltext.txt`, a byte-for-byte copy of the markdown.
There is no figure anywhere in this assignment. Read the markdown file itself as your
ground truth and check the transcription below against it.

Anchor text: `Ex. 2.5 | (20pts) Write a pseudo-code for exec(), fork(), waitpid(), and
exit() system calls.` and `Ex. 2.6 | (5pts) In Unix, there is a category of processes
called zombie process.`

## The questions, transcribed verbatim

> Ex. 2.5 | (20pts) Write a pseudo-code for exec(), fork(), waitpid(), and exit()
> system calls. Explain how these system calls are inter-related. Each pseudo-code is
> 2.5pts and the explanation is 2.5pts. Hint: write code to implement each system
> call, not use these system calls in some code.

> Ex. 2.6 | (5pts) In Unix, there is a category of processes called zombie process.
> What are these?

Note the arithmetic in 2.5: 4 × 2.5 = 10 for the pseudo-code and 2.5 for the
explanation is only 12.5, while the question is worth 20. Do not try to reconcile it —
answer what is asked: four pseudo-code bodies plus the inter-relation explanation, with
the explanation carrying real weight.

**Read the hint carefully — it is the whole trap in this question.** You are writing
the *kernel-side implementation* of each call: the code that runs inside the operating
system when a user process traps into `fork`, not a user program that calls `fork()`.
An answer that shows `pid = fork(); if (pid == 0) exec(...)` has answered the opposite
question and scores near zero.

The assignment's preamble also applies: *"You can utilize Google search and read
articles that help you to answer the questions. But you cannot just copy the answers,
put the answers in your own way."*

## What the deliverable is

**plain** (pseudo-code typeset as algorithms — there is nothing to execute, so do not
try to compile or run anything for 2.5).

### Ex. 2.5 — four pseudo-code bodies

Each should be a dozen-ish lines of kernel-level pseudo-code operating on the process
table / PCB, readable by a grader who knows Unix but not Linux source. Cover at least:

- **`fork()`** — allocate a PCB and a pid, fail with `EAGAIN` if either is exhausted;
  copy the parent's PCB fields (uid, cwd, umask, signal dispositions); copy or
  copy-on-write-share the address space; increment the reference count on every open
  file in the inherited descriptor table; link the child into the parent's child list;
  set the child's *saved return value* to 0 and the parent's to the child's pid (this
  one line is the whole "returns twice" phenomenon and should be visible in the code);
  put the child on the ready queue; return.
- **`exec(path, argv, envp)`** — open and validate the file (permission check,
  **magic number** → choose the loader; `ENOEXEC` if unrecognised); copy `argv`/`envp`
  into kernel space *before* the old address space is destroyed (they live in it);
  tear down the old address space; build the new one (text, data, bss, heap, stack),
  normally by mapping rather than reading; reset signal handlers to default while
  preserving ignored/blocked dispositions; close descriptors marked close-on-exec;
  handle set-uid; push `argv`/`envp` onto the new stack; set the saved PC to the entry
  point and return to user mode — note explicitly that on success it **does not
  return** to the caller, since the caller no longer exists.
- **`waitpid(pid, &status, options)`** — loop: scan the caller's children for one
  matching `pid`; if none exists at all, return `ECHILD`; if a matching child is in
  the **zombie** state, copy out its exit status, accumulate its resource usage,
  unlink it from the child list and free its PCB and pid (this is the *reaping* step),
  and return its pid; otherwise, if `WNOHANG` return 0, else block the caller on the
  wait channel until a child exit wakes it, then repeat.
- **`exit(status)`** — close all open descriptors (drop file reference counts),
  release the address space and most kernel resources, **re-parent surviving children
  to `init`** (and check whether any of them are already zombies, so `init` is woken),
  save the exit status and accounting information in the PCB, mark the process
  `ZOMBIE`, send `SIGCHLD` to the parent and wake it if it is blocked in wait, then
  call the scheduler and never return. The PCB survives — that is the point, and it is
  what 2.6 is about.

Typeset with `algorithm`/`algpseudocode` (i.e. `algorithmicx`) or `lstlisting`; all of
these are installed. Whatever you choose, put the `\usepackage` lines in
`OUTPUT/preamble.txt`, never in `answer.tex`, and give every float a `p4:`-namespaced
label.

### Ex. 2.5 — the inter-relation explanation

This part carries the marks that the pseudo-code alone cannot. Make the four calls one
mechanism rather than four bullet points: `fork` is the only way to get a new process
and `exec` the only way to change what a process is running, so *creating and running a
new program is necessarily the pair of them* — which is also why the split exists, as
it opens a window in the child where the shell can redirect descriptors before the new
image appears. `exit` and `waitpid` are the matching pair on the other end: the child's
status has to outlive the child, so `exit` leaves it in the PCB and `waitpid` collects
and frees it. A one-diagram-in-words sketch of the shell's lifecycle
(fork → child execs → parent waits → child exits → parent reaps) is the right way to
close it. A small state-transition figure is **optional**; only make one if you can do
it well as a vector PDF named `fig_p4_lifecycle.pdf`.

### Ex. 2.6 — zombies

A zombie is a process that has finished (`exit()` has run, its address space and
descriptors are gone) but whose PCB is still in the process table because its parent
has not yet called `wait`/`waitpid` to collect the exit status. Cover: why the kernel
keeps it (the status and accounting must survive to be reported, and the pid must not
be reused while it is still referable); what it costs (a process-table slot and a pid —
no memory, no CPU, and it cannot be killed, since it is already dead: `SIGKILL` does
nothing); how it is cleared (parent calls `wait`, or ignores/handles `SIGCHLD`
appropriately, or dies — whereupon `init` inherits it and reaps it); how it shows up in
practice (`Z` / `defunct` in `ps`); and the distinction from an **orphan**, which is a
*live* child whose parent died and which `init` adopts. Naming the failure mode —
a long-lived parent that never reaps leaks the process table until fork fails — is
worth one sentence.

## Length

25 points across two questions, most of it pseudo-code. The pseudo-code does not count
against the prose budget, but the explanation should be tight: aim for roughly 300–350
words for the 2.5 inter-relation explanation and about 190–220 words for 2.6. See R8
below: the failure mode here is restating in prose what the pseudo-code already says.

---

## Rules for workers

**Master: copy this whole section verbatim into every `problem.md` you write.**
Workers and worker validators never see this file; the brief is the only channel
that reaches both of them.

These are not style preferences. They are defects. A worker that breaks one has
not finished, and a validator that passes one has not done its job.

### R8 — Answer the question asked, at the length it deserves

Write the shortest answer that earns full marks, then stop. Concrete targets,
measured from a previous assignment after a careful human edit:

| question | target |
|---|---|
| a 5-point short answer | about 190 words; up to 290 if it has several sub-parts |
| a 10-point paper summary and critique | about 550 words |

Left alone, an answer comes out **1.5 to 2 times** these lengths. That is the
failure mode to watch for in yourself. The excess is never new substance; it is
always one of these four:

- **exhaustive enumeration** — four examples where the question needs one, six
  hardware mechanisms where three carry the argument;
- **summarising your own answer** — a closing sentence that restates the opening
  one. If a paragraph begins "so the model is X" and ends "the model is therefore
  X", delete the ending;
- **explaining the significance of your own answer** — the question asked *where*
  the magic number is stored, not why that location is efficient;
- **stating what you are about to do** — "the three binding times are worth
  naming", "it is worth noting that".

Em-dashes are a symptom rather than a cause, but they mark the places to look:
one every 70 words means the sentences are being extended rather than ended.

**Validator: count the words.** Compare against the target above and against what
the problem is worth. Over target by more than a quarter, with no sub-part that
justifies it, is a defect to be reported and fixed, at severity major. Do not pass
an answer because it is correct if it is also twice as long as it needs to be.

### R9 — Read past the quotation

When you quote or cite a source, read the sentences that follow the quote before
you build an argument on it. Stop at the quote and you will write a criticism the
source already answers, or attribute to an author a claim they did not make.

Both of these happened in a previous assignment and both were findable with one
grep by the person marking it:

- A paper was criticised for raising a security problem and leaving it there. The
  next sentence of the paper proposed two countermeasures. (The real criticism was
  available and stronger: one countermeasure reintroduced the central authority the
  design existed to remove, and the other was justified only "on a system that
  assumes no malicious processes".)
- A paper's closing section was described as claiming a system succeeded because
  it had no predefined objectives. It says nothing of the sort; it says the authors
  were grateful never to have had to satisfy someone else's requirements. The
  critique was aimed at an invented claim.

So: quote the source, then say what the source does next with it. Never assert that
an author "leaves the problem there", "never asks", or "does not address" something
without having read to the end of that discussion.

**Validator: for every quotation and every characterisation of what a source says
or fails to say, open the source and read the surrounding passage yourself.** A
quotation that is verbatim can still be used to support a claim the source
contradicts two sentences later. Confirming the words exist is not the check;
confirming the argument survives the context is.
