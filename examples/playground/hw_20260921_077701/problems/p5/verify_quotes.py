#!/usr/bin/env python3
"""Re-check every quotation and every quoted number in OUTPUT/answer.tex against
the three downloaded papers.

Run from PLAYGROUND:   python3 verify_quotes.py

NOTE ON TEXT EXTRACTION: `pdftotext -layout` interleaves the two columns of these
papers, so a sentence that wraps a line appears split by text from the other column
and a naive substring search fails. This script uses plain `pdftotext` (reading
order) and additionally undoes end-of-line hyphenation before searching. That is
why `papers/*_flow.txt` and not `papers/*.txt` are used here.
"""
import re, subprocess, sys, pathlib

P = pathlib.Path(__file__).parent / "papers"

def flow(name):
    src, dst = P / f"{name}.pdf", P / f"{name}_flow.txt"
    if not dst.exists():
        subprocess.run(["pdftotext", str(src), str(dst)], check=True)
    s = dst.read_text(errors="replace").replace("\u00ad", "")
    s = re.sub(r"-\s*\n\s*", "", s)          # undo hyphenation across line breaks
    return re.sub(r"\s+", " ", s)

docs = {n: flow(n) for n in ("lottery", "stride", "buttazzo")}

CHECKS = [
    # ---- 2-3 Lottery: quotations -------------------------------------------
    ("lottery", "converge toward their allocated values over longer time intervals"),
    ("lottery", "at a time scale of milliseconds to seconds"),
    ("lottery", "ensure fairness on a time scale of minutes"),
    ("lottery", "efficient lottery scheduling does not pose any challenging problems"),
    ("lottery", "A complete lottery scheduling system should protect currencies by using access control lists"),
    # ---- 2-3 Lottery: numbers ----------------------------------------------
    ("lottery", "average ratio of 13.42 : 1"),
    ("lottery", "for a 20 : 1 allocation was 19.08 : 1"),
    ("lottery", "executed 25378 and 12619 iterations/sec"),
    ("lottery", "17.19, 43.19, and 132.20 seconds"),
    ("lottery", "1.01 : 1 before"),
    ("lottery", "2.7% fewer iterations"),
    ("lottery", "0.8%"),
    ("lottery", "1.7%"),
    ("lottery", "1155.5 seconds"),
    ("lottery", "1135.5 seconds"),
    ("lottery", "25MHz MIPS-based DECStation 5000/125"),
    ("lottery", "quantum on this platform is 100 milliseconds"),
    ("lottery", "inflates its value by 1"),          # compensation ticket 1/f
    # ---- 2-4 Stride: quotations --------------------------------------------
    ("stride",  "lottery scheduling is conceptually simpler"),
    ("stride",  "effectively stateless"),
    ("stride",  "observed throughput ratios were consistently lower than specified"),
    ("stride",  "nearly identical to elements of rate-based flow-control algorithms"),
    ("stride",  "neither the standard Linux scheduler nor our prototype stride scheduler are particularly efficient"),
    ("stride",  "Our prototype also performs a linear scan"),
    ("stride",  "We did not implement support for higher-level abstractions such as ticket transfers and currencies"),
    # ---- 2-4 Stride: numbers -----------------------------------------------
    ("stride",  "the observed ratios are within 1% of the ideal"),
    ("stride",  "within 5% of the ideal"),
    ("stride",  "2409.18 and 802.89 iterations/sec"),
    ("stride",  "actual ratio of 3.001:1"),
    ("stride",  "maximum absolute error of only 4.5"),
    ("stride",  "absolute error of 50"),
    ("stride",  "ranging from 1 to 194 quanta"),
    # Fig. 12 caption. pdftotext renders the Computer Modern math decimal point
    # as ':' and drops the mu/sigma glyphs, so "20.13" extracts as "20:13".
    # All four values were additionally confirmed by eye from the rendered page
    # (papers/fig12_cap.png, fig12_cap2.png, from `pdftoppm -f 15 -l 15 stride.pdf`):
    #   1-ticket client -- lottery mu=20.13 sigma=19.64 ; stride mu=20.00 sigma=0.01
    ("stride",  "= 20:00,"),                          # stride mu, 1-ticket client
    ("stride",  "= 0:01"),                            # stride sigma
    ("stride",  "= 20:13,"),                          # lottery mu
    ("stride",  "= 19:64"),                           # lottery sigma
    ("stride",  "difference was always less than 0.2%"),
    ("stride",  "Fewer than 300 lines"),
    ("stride",  "Linux 1.1.50 kernel on a 25MHz i486"),
    # ---- 2-1 Buttazzo: quotations ------------------------------------------
    ("buttazzo", "this example does not prove that EDF always introduces less jitter"),
    ("buttazzo", "deciding which one is better is highly application dependent"),
    ("buttazzo", "both RM and EDF are not very well suited to work in overload conditions"),
    ("buttazzo", "can be of little use if we do not know a priori which task is going to overrun"),
    ("buttazzo", "the PDC requires more computational steps"),
    ("buttazzo", "the real advantage of RM with respect to EDF is its simpler implemen"),
    # ---- 2-1 Buttazzo: numbers ---------------------------------------------
    ("buttazzo", "not greater than 256"),
    ("buttazzo", "can be performed in O(1)"),
    ("buttazzo", "= ln 2 ≃ 0.69"),
    ("buttazzo", "U = 0.9"),
    ("buttazzo", "range of 10"),                      # periods uniform in [10,100]
    ("buttazzo", "U = 4/8 + 6/12 + 5/20 = 1.25"),
    ("buttazzo", "T̄i = Ti U"),
    ("buttazzo", "C1 = 2, C2 = 3, C3 = 1, C4 = 1"),   # transient-overload example
    ("buttazzo", "T1 = 5, T2 = 9, T3 = 20, T4 = 30"),
    ("buttazzo", "an overrun of 1.5 time units"),
    ("buttazzo", "the task that misses its deadline is not the one with the longest period"),
    ("buttazzo", "C1 = 2,"),                          # jitter example
    ("buttazzo", "T1 = 6, T2 = 8, T3 = 12"),
    ("buttazzo", "equal to 0, 2,"),                   # RM jitters 0,2,8
    ("buttazzo", "1, 2, and 3"),                      # EDF jitters
]

fail = 0
for doc, q in CHECKS:
    ok = q in docs[doc]
    if not ok:
        fail += 1
    print(f"{'OK  ' if ok else 'MISS'}  {doc:9s} | {q}")

print(f"\n{len(CHECKS) - fail}/{len(CHECKS)} verified, {fail} missing")
sys.exit(1 if fail else 0)
