# p4 — Ex. 3.9 notes

## Channel reconciliation (R7)
Source is PaperList.xlsx (a spreadsheet), not a figure-bearing PDF. manifest.json
reports n_images=0 on every page, so there are no extracted figure files; the three
channels available are the CSV export, page_00N.txt, and page_00N.png.

- CSV (`ingest/csv/PaperList.csv`): rows 3-1..3-7, topic cell populated only on 3-1.
- page_003.txt: titles column-major; title of 3-6 ("Machine-Independent Virtual
  Memory Management for Paged Uniprocessor and Multiprocessor / Architect") is
  dumped at the very bottom of the page, out of order. Reading this channel alone
  makes Memory Management look like six papers.
- page_005.png: topic column rendered; "Memory Management" is one tall merged block.
- FOURTH, decisive check: merged-cell ranges read straight out of the xlsx XML
  (`xl/worksheets/sheet1.xml`): <mergeCell ref="C20:C26"/>. Rows 20-26 = 7 data rows
  = papers 3-1 .. 3-7. Invariant: 6 merges for 6 topics; C2:C12 (11) + C13:C19 (7)
  + C20:C26 (7) + C27:C36 (10) + C37:C46 (10) + C47:C54 (8) = 53 = number of data
  rows in the CSV. Confirms SEVEN Memory Management papers.

Brief and assignment text agree verbatim on the question wording. No discrepancy.

## What this problem needs
plain. No computation, no figure. The work is: obtain three of the seven papers IN
FULL, read them, write ~400-450 words each (summary ~60% / critique ~40%), with
verified citations (authors, venue, year) taken from the paper itself, not memory.

## Plan
1. Download candidate papers as PDFs/HTML into papers/. Record each in downloads.md.
2. Verify full text present (not an abstract stub): page count, section headings.
3. Pick three with the best critical material; read each end-to-end.
4. For every criticism, locate the passage where the paper addresses the issue and
   read past it (R9) before asserting an omission.
5. Write answer.tex, word-count it, lint OUTPUT.

## Papers chosen and why
3-1 Denning (theory), 3-6 Rashid et al. (kernel structure), 3-4 Navarro et al.
(hardware-driven performance). All three obtained as full PDFs and read end to end;
3-2 (WSCLOCK) and 3-3 (Multics) were not pursued once three full texts were in hand.

## Quotation verification (R9)
scripts/verify_quotes.py re-checks every quoted string against the extracted paper
text after de-hyphenating line breaks and normalising the fi/fl ligatures. All eight
quotations verified verbatim. For each criticism I also read the sentences that follow
the quoted passage:
- Denning sharing: he says charging for overlapping working sets "is still an open
  question, and is under investigation" -- so I do NOT claim he ignores sharing.
- Mach: no occurrence of trust/security/malicious/deadlock anywhere in the paper, so
  the external-pager trust question genuinely is absent; I did not build on it, the
  shadow-chain and missing-counterfactual points are stronger.
- Superpages 4.7: after rejecting the SHA-1 scheme they name two optimisations and
  defer them to future work -- that "what the paper does next" is the critique.
