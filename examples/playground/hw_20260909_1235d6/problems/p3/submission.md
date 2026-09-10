# p3 — Ex. 1.9 submission

## What the problem asked

> Ex. 1.9 (30pts) | Pick three papers from 'OS History and Architecture' in the paper list.
> Read, summarize, and critically judge them. Write at least 1/3 page for each paper's
> summarization and judgment. (10pts for each paper)

Ground truth is `input/hw_questions.md` line 37. **The brief's transcription matches it
verbatim — no discrepancy.** The global instruction on line 1 ("you cannot just copy the
answers, put the answers in your own way") applies, so nothing is lifted from the papers'
abstracts.

**Independent re-verification of the paper-list trap.** The brief warned that the `Topics`
column uses merged cells and told me the answer. I did not take its word; I re-checked all
three channels myself and reached the same conclusion:

1. `ingest/csv/PaperList.csv` — `OS History and Architecture` appears only on row 1-1; rows
   1-2..1-11 are blank; `Scheduling` reappears on 2-1. One contiguous blank run ⇒ a merged
   cell spanning 1-1..1-11.
2. `ingest/pages/PaperList/page_001.png` — the Paper ID column is colour-banded, and this is
   evidence independent of the CSV: 1-1 through 1-11 form one green band, 2-1 starts a blue
   one.
3. `ingest/pages/PaperList/page_005.txt` — the topic labels in order.

So 'OS History and Architecture' = papers 1-1 .. 1-11, as the brief said.

**One small correction to the brief.** It states that page_005.txt lists "the five topic
labels in order, and their order matches the ID prefixes 1-, 2-, 3-, 5-, 4-". What that file
actually contains is: OS History and Architecture / Scheduling / Memory Management / Storage
and File Systems / Threads, Events, Concurrency, Synchronization. `Distributed Systems`
(group 6-, which does exist in the CSV) is missing from that text channel entirely. This is a
column-major PDF-extraction artifact and does not affect group 1 membership, which channels
1 and 2 establish on their own. Flagging it only because the brief cited that file as
corroboration and it is a weaker witness than advertised.

## What I decided it needed

**plain** — prose only. No code, no diagram, no figure.

There is no quantity to compute, nothing to plot, and no figure in the assignment to
transcribe. The only real "data gathering" is downloading and reading the three papers, which
I did. (I did use the shell for PDF text extraction and a Crossref metadata lookup, but
nothing in the answer is a computed result, so there is no number for the validator to
recompute from a script of mine — every number in the answer is a fact quoted from a paper,
and I list them all below with line references.)

## What I did

Picked **1-10** (Dijkstra, "THE", 1968), **1-2** (Ritchie & Thompson, UNIX, 1974) and
**1-3** (Engler, Kaashoek & O'Toole, Exokernel, 1995) — the trio the brief suggested — because
they form one continuous argument about where structure belongs: layers → uniform
abstractions → no fixed abstractions at all. That arc makes the "critically judge" half
substantive instead of three disconnected book reports.

Downloaded all three PDFs (ACM DL returns 403 to curl, so mirrors were used; each mirror was
verified to be the genuine paper by checking title, author line and body text *inside* the
PDF, not by trusting the URL). Extracted layout text with `pdftotext -layout` and read the
bodies — mechanisms, evaluation sections, stated limitations and conclusions — not the
abstracts. For each paper I hunted specifically for the things a critical judgment needs:
what was actually measured, what was assumed, and what the authors themselves conceded.

Wrote ~800 words per paper (summary + judgment), each naming its Paper ID explicitly in the
heading, plus a short comparative closing section.

**Anti-plagiarism:** the prose is mine throughout. Direct quotation is confined to short
phrases that are the actual object of criticism (e.g. Dijkstra's "guaranteed to be flawless",
the exokernel authors' "best case" concession), each marked with quotation marks. No abstract
is paraphrased.

## Intermediate steps and code

No analysis scripts — this is a prose problem. The reproducible commands are:

- `papers/` — the four downloaded PDFs. Every download is recorded in `downloads.md`.
- `papers/txt/*.txt` — text extracted with
  `pdftotext -layout papers/<name>.pdf papers/txt/<name>.txt`. This is what I read.
- `papers/ewd_png/p-0{3,4,5}.png` — `pdftoppm -r 150 -png -f 3 -l 5 papers/the_ewd196_scan.pdf`.
  Used as a second channel to confirm the CACM text layer, which has heavy OCR noise
  (it renders "correctness" as "eon'eetness", "von Neumann" as "yon Neumann").
- Citation verification: `curl -s https://api.crossref.org/works/<DOI>` for the three DOIs
  `10.1145/363095.363143`, `10.1145/361011.361061`, `10.1145/224056.224076`. I did this
  because the PDFs I have are re-paginated 1..N and do **not** show the original ACM page
  numbers, so I could not have read pp. 341--346 / 365--375 / 251--266 off them.
- `build/` — LaTeX compile check. `build/bare.tex` inputs `answer.tex` into a bare
  `\documentclass{article}` with **zero packages** and compiles clean (exit 0, 0 errors),
  which is why I ship no `preamble.txt`.

## Results

Nothing in the answer is a value I computed; every number is a fact read out of a paper.
Listing them so the validator can spot-check rather than re-derive. Line numbers are into
`papers/txt/<file>.txt`.

**Paper 1-10 (the_cacm1968.txt)** — EL X8, 2.5 µs core cycle, 27-bit words, 32K core, 512K-word
drum (L46--60); six people at half-time (L25--26); not a multi-access system, ALGOL 60 library
(L74--78); levels 0--5 with level 5 "not implemented by us" (L157--189); one error per 500
instructions, located within 10 minutes (L69--73); **"the resulting system is guaranteed to be
flawless"** (L73--75); the drum-segment pinning precaution against "unproductive page flutter"
(L361--373); "the larger the project, the more essential the structuring" (L256--257);
"Deadly Embrace" (L393--396).

**Paper 1-2 (unix_cacm1974.txt)** — 144K core / UNIX occupies 42K (L57--58); 40,000 dollars and
"less than two man years", ~40 installations since Feb 1971 (L11--12, L28); rewritten in C
summer 1973, "about one third greater" (L88--91); seven protection bits — rwx for owner and
for all other users (no group), set-user-ID, super-user exempt (L133--151, L169--175);
i-node with eight device addresses, indirect blocks of 256, max file 8·256·512 = 2^20 bytes
(L298--311); **section 4.1 — the entire performance evaluation:** 7621-line assembly, 35.9 s,
212 lines/sec, 63.5% / 16.5% / 20%, and "We will not attempt any interpretation of these
figures nor any comparison with other systems" (L336--347); pipes "not a completely general
mechanism ... must be set up by a common ancestor" (L351--353); charging dodged by "not
charging any fees at all" (L318--321); "not designed to meet any predefined objectives"
(Perspective §8); statistics 72 users / 14 simultaneous / 4400 files / 1800 commands per day /
4.3 CPU hours / 75 logins / ~98% uptime / longest run ~two weeks, and chess at 5.3% of CPU
(§9.1--9.5).

**Paper 1-3 (exokernel.txt)** — Cao et al. 45% (L~100); secure bindings / visible revocation /
abort protocol (L64--69, §3); software TLB (L315--321); packet filters as downloaded code
(L322--334); repossession vector and a guaranteed reserve of five to ten pages (L~440);
Aegis and ExOS on MIPS DECstations, ExOS implements ARP/RARP, IP, UDP, NFS (L448--465);
**"our prototype system has no real users"** (L~465); file system "under development"
(L~464); exception dispatch 1.5 µs on DEC5000/125, five times the best reported, ~two orders
of magnitude vs Ultrix (L86--95, L633--661); protected control transfer almost seven times the
best reported (L90--93); DPF 1.5 µs vs MPF 35.0 µs (Table 7, L726--730); stride scheduler
"less than 100 lines of code" (L~1028); **"do not consider cold start misses in the cache or
TLB, and therefore represent a best case"** (L538--541); **"ExOS do not offer the same level of
functionality as Ultrix. We do not expect these additions to cause large increases in our
timing measurements"** (L499--501); ExOS VM "does not handle swapping" (L~825); 150×150 matrix
multiply (Table 9, L803--812); ten-to-100× on primitives (abstract, L27).

**Citations** (verified against Crossref, not guessed):
- 1-10: CACM **11**(5), May 1968, pp. **341--346**. Independently corroborated by the EWD196
  scan's own copyright page: "Commun. ACM 11 (1968), 5: 341--346".
- 1-2: CACM **17**(7), July 1974, pp. **365--375**. Corroborated by the PDF's running footer.
- 1-3: **SOSP '95** (Fifteenth ACM SOSP), pp. **251--266**, 1995.

**Compile check:** `answer.tex` inputs into a bare `\documentclass{article}` with no packages
and compiles with exit 0 and zero errors; ~5 pages of set text at 11pt. Lengths: 812 / 875 /
802 words for papers 1-10 / 1-2 / 1-3, plus a 180-word comparative section. The requirement
is 1/3 page (~300--400 words) each, so each paper clears the floor roughly 2×.

**One LaTeX defect I found and fixed:** `\$` (which I had used for "$40,000") pulls in the TS1
text-companion font `tcrm1095`, which on this machine only exists as METAFONT source and
cannot be cached because `~/.TinyTeX` is read-only — it is a *fatal* compile error, not a
warning. Since I cannot know whether the master's preamble loads `fontenc`/`lmodern`, I
removed the dollar sign and wrote "40,000 dollars" instead. Worth flagging to the master: any
worker who writes `\$` will break the assembled compile on this box.

## Deliverables

- `OUTPUT/answer.tex` — the fragment. `\section*` + three `\subsection*` (one per paper) +
  comparative section + manual reference list. All five labels namespaced: `p3:sec:ex19`,
  `p3:sec:the`, `p3:sec:unix`, `p3:sec:exokernel`, `p3:sec:together`, `p3:sec:refs`.
- No `preamble.txt` — deliberately, because the fragment needs no packages at all.
- No figures — the problem is prose only.
- `lint_output.py` passes (exit 0); OUTPUT contains `answer.tex` and nothing else.

## Where I am least confident

1. **The historical claims in the judgments are mine, not the papers'.** Specifically: that
   strict level ordering did not survive because real systems have cyclic dependencies
   (pager↔disk driver↔memory); that named pipes and sockets were bolted on later because the
   pipe's common-ancestor restriction was a real limit; and that hardware virtualization
   within a decade undercut the exokernel's dismissal of VM/370 while unikernels vindicated
   the idea. These are, I believe, the standard and defensible reading, and the assignment
   invites exactly this kind of judgment — but they are argued from general knowledge of the
   field, not cited to a source I downloaded and read. A validator is entitled to push back
   on any of the three. The *criticisms grounded in the papers themselves* (the "flawless"
   claim, the pinning precaution, section 4.1, the "best case" and "no real users"
   admissions) are the load-bearing ones and are all quoted above with line references.

2. **The CACM text layer for Paper 1-10 is OCR and is noisy.** I cross-checked the quotes I
   actually use against the EWD196 manuscript scan and they hold, with one difference worth
   recording: the manuscript reads "the resulting system **will be** guaranteed to be
   flawless" while the published CACM text reads "**is** guaranteed to be flawless". I quote
   the CACM wording, since the CACM article is the paper on the list. The difference does not
   change the point.

3. **I did not verify the exokernel's page numbers from the PDF itself** — the MIT PDOS copy
   is renumbered 1..16. pp. 251--266 comes from Crossref. Same for the other two, though for
   those the PDFs' own footers agree.

4. **Word count is roughly 2.4× the stated floor per paper.** The brief warned against
   padding. I judged that "at least 1/3 page" for *both* a summary and a critical judgment
   worth 10 marks justifies ~800 words, and I kept every paragraph doing work — but if the
   validator reads any section as bloated, the compressible parts are the mechanism inventories
   in the summaries, not the judgments.
