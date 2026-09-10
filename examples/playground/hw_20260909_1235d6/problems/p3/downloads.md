# Downloads and installs for this problem

One line per item: `- <name> | <how> | <path> | <why>`

All items are paper PDFs downloaded in order to actually read the papers. No package was
installed and no venv was created — this problem is plain prose with no code or figures.
Everything lives under `PLAYGROUND/papers/`.

- Dijkstra, "The Structure of the THE-Multiprogramming System" (CACM 1968), text-layer PDF | `curl -sL https://sites.cs.ucsb.edu/~rich/class/cs270/papers/dijkstra-the.pdf` | `papers/the_cacm1968.pdf` | Paper 1-10; the searchable copy of the CACM article I actually read.
- Dijkstra, EWD196 manuscript scan of the same paper (UT Austin EWD archive) | `curl -sL https://www.cs.utexas.edu/users/EWD/ewd01xx/EWD196.PDF` | `papers/the_ewd196_scan.pdf` | Paper 1-10; second channel. The scan has no usable text layer (205 chars) but its copyright page independently confirms the citation "Commun. ACM 11 (1968), 5: 341-346".
- Ritchie & Thompson, "The UNIX Time-Sharing System" (CACM 1974) | `curl -sL https://dsf.berkeley.edu/cs262/unix.pdf` | `papers/unix_cacm1974.pdf` | Paper 1-2; the paper I read.
- Engler, Kaashoek & O'Toole, "Exokernel: An Operating System Architecture for Application-Level Resource Management" (SOSP 1995) | `curl -sL https://pdos.csail.mit.edu/6.828/2008/readings/engler95exokernel.pdf` | `papers/exokernel.pdf` | Paper 1-3; the paper I read (hosted by the authors' own group, MIT PDOS).

Note: `dl.acm.org` returns HTTP 403 to curl for all of these, so mirrors were used. Each
mirror was verified to be the genuine paper by checking its title, author line and body text
inside the PDF, not by trusting the URL.
