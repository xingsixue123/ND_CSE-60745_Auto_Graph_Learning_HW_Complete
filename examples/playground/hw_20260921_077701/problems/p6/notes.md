# p6 — notes

## What the problem needs
**plain** only. No code, no diagram. Ex. 2.8 asks for three *self-found* scheduling
papers, each with a summary and a critical judgment, >= 1/3 page each, 7.5 pts each.
Target per brief: 400–450 words per paper, ~1250–1400 total, plus a one-line note on
how I searched, plus a reference list.

## Ground truth check
Assignment file `/home/xing/project/auto_hw_complete/input/hw2_instruction.md` line 38
reads exactly: "Ex. 2.8 | (22.5pts) Search for three papers on the topic of
'Scheduling'. Read, summarize, and critically judge them. Write at least 1/3 page for
each paper's summarization and judgment. (7.5pts for each paper)". Matches the brief
verbatim. Preamble (line 1) confirms the "own words" constraint. No figures anywhere.
PaperList.csv confirms the Scheduling group is 2-1..2-7 (2-1 carries the merged
`Scheduling` label; 2-2..2-7 blank but in the same group; row 3-1 starts the next
topic). So the exclusion set is those seven.

## The three papers chosen (spread: theory / kernel / datacenter)
1. Liu & Layland, JACM 1973 — classical real-time scheduling theory (RM + deadline
   driven). NOT 2-1 ("Rate Monotonic vs. EDF: Judgment Day") — that is a 2003 IEEE
   survey comparing the two; this is the 1973 origin paper. Distinct work, distinct
   authors. Justified as "the primary source the list's 2-1 argues about".
2. Lozi et al., EuroSys 2016 — Linux CFS load-balancer bugs on multicore.
3. Kaffes et al., Shinjuku, NSDI 2019 — microsecond-scale preemptive datacenter
   scheduling.
None of these is on the list, none is a second lottery/stride paper.

Risk noted: #1 is *topically* adjacent to 2-1. Mitigation — 2-1 is a different paper
(Buttazzo 2005, IEEE TIC); I say explicitly why I picked the 1973 primary source and
critique it on its own 1973 terms, not as a rehash of the RM-vs-EDF debate.

## Method
Download all three PDFs into PLAYGROUND/papers/, read them with the Read tool /
pymupdf, pull every number I quote out of the actual text, record page numbers in
PLAYGROUND/evidence.md. No number goes into answer.tex that I have not seen in the
PDF.
