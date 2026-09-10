# p3 — Ex. 1.9 validator checklist

## Round 1
Verdict: PASS

### What I verified independently (not by trusting the worker's notes)

**Question ground truth.** `input/hw_questions.md` line 37 read directly. The brief's
transcription and the worker's restatement both match verbatim. Note that Ex. 1.0 (line 41)
is a *different* problem — "search for three papers" on the same topic — so p3 correctly
answered the "pick from the paper list" variant.

**Paper-list ID mapping.** Read `ingest/csv/PaperList.csv` myself. Confirmed
1-2 = The UNIX Time-Sharing System, 1-3 = Exokernel, 1-10 = The Structure of the
"THE"-Multiprogramming System. Confirmed the merged-cell trap: `OS History and Architecture`
appears only on row 1-1, rows 1-2..1-11 are blank, `Scheduling` resumes at 2-1 — one
contiguous run, so group 1 = 1-1..1-11. The worker's three picks are all in-group.

**PDF authenticity.** All three PDFs are the genuine papers, verified by title/author line
and body text inside each file, not by URL.

**Factual claims — I re-checked roughly 40 distinct claims against the extracted paper text.
Every one is correct.** Spot-list:

- *THE (1-10):* EL X8, 2.5 µs / 27 bits / 32K core / 512K-word drum (L34-42); "a group of six
  people of, on the average, half-time availability"; not a multi-access system, ALGOL 60
  library; level 0 processor+real-time clock, 1 segment controller, 2 message interpreter,
  3 peripheral buffering, 4 user programs, 5 "the operator (not implemented by us)"
  (L155-189) — the level assignments match the paper exactly; "harmonious cooperation is
  mainly proved in roughly [three stages]" with numbered (1)(2)(3) (L354-382); "Deadly
  Embrace" (L393); one error per 500 instructions, located within 10 minutes (L69-72);
  testing "Starting at level 0 ... each time adding (a portion of) the [next level]" (L221).
- The load-bearing quote is real and in context: *"At the time this was written the testing
  had not yet been completed, but the resulting system is guaranteed to be flawless."*
  (L72-75). The worker's criticism of it is fair.
- The pinning observation is the best thing in the answer and it is verbatim supported:
  "special precautions have been taken to ensure that the segment asked for remains in core
  at least until the requesting process has effectively accessed the segment concerned.
  Without this precaution finite tasks could be forced to generate an infinite number of
  tasks for the segment controller, and the system could get stuck in an unproductive page
  flutter." (L362-373). Also "the larger the project, the more essential the structuring!"
  (L256).
- *UNIX (1-2):* 144K core / UNIX occupies 42K; $40,000; "less than two man years"; ~40
  installations since February 1971; rewritten in C summer 1973, "about one third greater"
  (L91); "a set of seven protection bits. Six of these specify independently read, write, and
  execute permission for the owner of the file and for all other users" + seventh =
  set-user-ID + super-user exempt (L133-151) — matches the answer's "no group in this
  version"; "threefold advantage" for special files (L128-152); i-node "eight device
  addresses", "block of 256 addresses", "8·256·512, or 1,048,576 (2^20)" (L300-310);
  "Files are named by sequences of 14 or fewer characters" (L85) — the 14-char claim is
  supported; section 4.1 in full: 7621 lines, 35.9 sec, 212 lines/sec, 63.5/16.5/20.0, and
  "We will not attempt any interpretation of these figures nor any comparison with other
  systems, but merely note that we are generally satisfied" (L339-347); pipes "not a
  completely general mechanism since the pipe must be set up by a common ancestor" (L351);
  "avoids the issue by not charging" (L327); Perspective: "the success of UNIX is largely due
  to the fact that it was not designed to meet any predefined objectives" (L576-580);
  §9 stats 72 / 14 / 4400 / 1800 / 4.3 / 75 / 98 percent / two weeks / chess 5.3% (L645-675).
- *Exokernel (1-3):* Cao et al. 45% (L106-110); abstract "ten to 100 times faster than in
  Ultrix" (L26-28) — I initially suspected the answer's "ten-to-100×" was a misread of the
  "five to 40 times" figure, but the answer uses the correct one; that 40× figure is a
  separate claim about application-level VM/IPC primitives; "Aegis's protected control
  transfer is almost seven times faster than the best reported implementation" and "exception
  dispatch is five times faster ... roughly two orders of magnitude faster than in Ultrix
  4.2" (L86-96); 1.5 µs on DECstation5000/125 (L633); Table 7 MPF 35.0 / DPF 1.5 (L726-728);
  Table 9 150x150 matrix multiplication (L811); stride scheduler "less than 100 lines of
  code" (L1006); reserve of "five to ten physical [pages]" (L427); software TLB / STLB
  (L316-320, L715-720); abort protocol, repossession vector, floating-point state not live
  (L68, L413, L434); ARP/RARP, IP, UDP, NFS (L454); dynamic code generation for DPF (L759).
  The three concessions the judgment rests on are all verbatim: "our prototype system has no
  real users" (L456); "ExOS do not offer the same level of functionality as Ultrix. We do not
  expect these additions to cause large increases in our timing" (L499-500); "represent a
  'best case'" (L541).

**Citations.** Verified independently via Crossref, not by trusting the worker:
10.1145/363095.363143 → CACM 11(5), May 1968, 341–346; 10.1145/361011.361061 → CACM 17(7),
July 1974, 365–375; 10.1145/224056.224076 → SOSP '95, 251–266. All three match answer.tex.

**Second channel for 1-10.** Opened `papers/ewd_png/p-03.png` myself. The EWD196 scan is
genuine and independently confirms the EL X8 hardware specs. The worker's cross-check claim
is real, not asserted.

**Deliverable type.** Correctly judged **plain** — no computed quantity, nothing to plot, no
figure in the assignment to transcribe. No figure is required, so the absence of one is not a
defect here.

**Requirements coverage.** Three papers, each with an explicit `\textbf{Summary.}` and
`\textbf{Critical judgment.}`; judgments are genuine criticism, not praise. Paper IDs stated
explicitly in the intro and in every heading (the master needs these). Comparative closing
section present. Word counts (my own count, macros stripped): 831 / 848 / 783 + 177
comparative + 123 references = 2837 total, i.e. each paper ~2× the ~400-word floor.

**LaTeX / R5 compliance.** No `\documentclass`, `\usepackage`, or `document` environment.
All six labels namespaced `p3:`. No figure includes, no absolute paths. I compiled the
fragment myself in a bare `\documentclass[11pt]{article}` wrapper with **zero packages**:
exit 0, zero `!` errors, 7 pages.

**Output hygiene.** `python3 framework/tools/lint_output.py` → `OUTPUT LINT OK`, exit 0.
OUTPUT contains `answer.tex` and nothing else. `downloads.md` records all four downloads with
name/how/path/why per R3. No venv or package install was made, correctly.

**Worker's `\$` finding — verified true.** I reproduced it: `\$` in a bare 11pt article pulls
TS1 `tcrm1095`, which exists only as METAFONT source, and `~/.TinyTeX` being read-only makes
it a *fatal* error (exit 1, "Font tcrm1095 at 600 not found"). The workaround ("40,000
dollars") is justified and the warning is worth relaying to the master.

### Defects
- [1.1] Four short unquoted verbatim spans lifted from the source papers, in an answer that
  is otherwise clearly original prose. The assignment's global instruction says "you cannot
  just copy the answers, put the answers in your own way", so these should be quoted or
  reworded. | `OUTPUT/answer.tex` | severity: minor
    - L42: "can only generate tasks for processes at lower levels" (THE, L370-372)
    - L64-65: "number of tasks for the segment controller" + "the system" (THE, L371-373) —
      partially reworded already ("infinite"→"unbounded", page flutter→"thrash")
    - L102: "all links to a file have equal status" (UNIX, L~228)
    - L175-176: "the processor is explicitly revoked at the end of a time slice" (Exokernel,
      L427) — 12 words, the longest of the four and the one most worth fixing
  Each is a short technical mechanism statement rather than a lifted argument, and the
  analytical content throughout is the worker's own, which is why this is minor and not
  blocking.
- [1.2] `submission.md` L138 claims the fragment sets "~5 pages"; a bare 11pt article wrapper
  produces 7. Inaccuracy is in the notes, not the deliverable, and errs toward exceeding the
  length requirement. | `submission.md` | severity: minor
- [1.3] All six `\label{}`s attach to starred (`\section*`/`\subsection*`) headings, which
  produce no number, so the labels are inert. Harmless and correctly namespaced; noted only
  because they are dead weight. | `OUTPUT/answer.tex` | severity: minor

### Resolved since last round
(none — first round)

### Still outstanding
[1.1], [1.2], [1.3] — all minor. None blocks delivery to the master. Per the validator
brief, remaining objections are cosmetic/hygiene only, so this passes.
