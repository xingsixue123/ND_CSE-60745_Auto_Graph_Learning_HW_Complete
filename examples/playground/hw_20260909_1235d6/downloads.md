# Run-level downloads and installs — job hw_20260909_1235d6

Rule R3 record for the whole run. Format: `- <name> | <how> | <path> | <why>`

**No software was installed anywhere in this run.** No venv, no `pip install`, no `conda`,
no `tlmgr`. Everything used (`pdflatex`/`latexmk` from TinyTeX, `pdftoppm`, `pdftotext`,
`pdfinfo`, `python3`) was already present per `framework/env.md`. The master agent itself
downloaded nothing.

The only downloads in this run are six paper PDFs, fetched by the p3 and p4 workers so that
they could actually read the papers rather than write from memory of the titles. All six
live inside PLAYGROUND and are reproduced here from the per-problem records
(`problems/p3/downloads.md`, `problems/p4/downloads.md`), which remain authoritative.

## Ex. 1.9 (worker p3) — papers from the supplied list

Base path: `problems/p3/papers/`

- Dijkstra, "The Structure of the THE-Multiprogramming System" (CACM 1968) | `curl -sL https://sites.cs.ucsb.edu/~rich/class/cs270/papers/dijkstra-the.pdf` | `problems/p3/papers/the_cacm1968.pdf` | Paper 1-10; the searchable copy actually read.
- Dijkstra, EWD196 manuscript scan of the same paper | `curl -sL https://www.cs.utexas.edu/users/EWD/ewd01xx/EWD196.PDF` | `problems/p3/papers/the_ewd196_scan.pdf` | Paper 1-10, second channel; no usable text layer, but its copyright page independently confirms the citation CACM 11 (1968), 5: 341-346.
- Ritchie & Thompson, "The UNIX Time-Sharing System" (CACM 1974) | `curl -sL https://dsf.berkeley.edu/cs262/unix.pdf` | `problems/p3/papers/unix_cacm1974.pdf` | Paper 1-2.
- Engler, Kaashoek & O'Toole, "Exokernel" (SOSP 1995) | `curl -sL https://pdos.csail.mit.edu/6.828/2008/readings/engler95exokernel.pdf` | `problems/p3/papers/exokernel.pdf` | Paper 1-3; hosted by the authors' own group, MIT PDOS.

## Ex. 1.0 (worker p4) — papers found by search, none on the list

Base path: `problems/p4/papers/`

- Corbato & Vyssotsky, "Introduction and Overview of the Multics System" (AFIPS FJCC 1965) | `curl -sSL https://courses.cs.washington.edu/courses/cse451/20wi/readings/MulticsDesign.pdf` | `problems/p4/papers/multics_fjcc1965.pdf` | Paper 1 of three for Ex 1.0.
- Accetta et al., "Mach: A New Kernel Foundation for UNIX Development" (USENIX Summer 1986) | `curl -sSL https://cseweb.ucsd.edu/classes/wi11/cse221/papers/accetta86.pdf` | `problems/p4/papers/mach_usenix1986.pdf` | Paper 2 of three.
- Baumann et al., "The Multikernel" (SOSP 2009) | `curl -sSL https://www.sigops.org/s/conferences/sosp/2009/papers/baumann-sosp09.pdf` | `problems/p4/papers/multikernel_sosp2009.pdf` | Paper 3 of three; official ACM SIGOPS open copy.

## Notes

`dl.acm.org` returns HTTP 403 to `curl` for all of these, so university and author-group
mirrors were used instead. Each mirror was verified to be the genuine paper by reading the
title, author line and body text inside the downloaded PDF, not by trusting the URL.

Derived scratch files also live under those `papers/` directories: `.txt` text extractions and
`.png` figure crops (`fig6_zoom.png`, `fig7_hi.png`, `tab23_zoom.png`, ...) produced locally
with `pdftotext`/`pdftoppm`/PIL in order to read figures at native resolution. Nothing was
downloaded to produce them, and none of them is in OUTPUT.

Cleanup: deleting `playground/hw_20260909_1235d6/` removes everything listed above. Nothing
was written outside PLAYGROUND and OUTPUT.
