#!/usr/bin/env python3
"""Extract full text of each downloaded paper, page-delimited, for reading."""
import pymupdf, pathlib
d = pathlib.Path(__file__).resolve().parent.parent
for pdf in sorted((d / "papers").glob("*.pdf")):
    doc = pymupdf.open(pdf)
    out = []
    for i, pg in enumerate(doc, 1):
        out.append(f"\n===== {pdf.name} page {i}/{doc.page_count} =====\n")
        out.append(pg.get_text())
    tgt = d / "papers" / (pdf.stem + ".txt")
    tgt.write_text("".join(out))
    print(pdf.name, doc.page_count, "pages ->", tgt.name, len("".join(out)), "chars")
