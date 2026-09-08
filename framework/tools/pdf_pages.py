#!/usr/bin/env python3
"""Three-channel PDF reader: page images, extracted text, AND native-resolution figures.

Both of the obvious channels are lossy in opposite directions.  Text extraction
silently drops every figure and mangles equation and table layout.  A rendered page
image carries the figures but gets downscaled when an agent reads it, and a graph
whose node labels are 8pt on the page becomes unreadable -- an agent that answers from
it is guessing.

So this also pulls every embedded figure out at its **native resolution** into its own
file.  That is the channel to use when a question refers to "the following graph": the
figure comes out at the size it was authored at, not at whatever survives a page
downscale.

Usage:
    python3 pdf_pages.py <file.pdf> --outdir <dir> [--dpi 200]

Writes into <dir>:
    page_001.png        rendered whole page
    page_001.txt        text extracted from that page
    page_001_fig_01.png embedded figure, native resolution   <-- read these for figures
    alltext.txt         all text, page-delimited
    manifest.json

Page numbers are the RENDERED index (1-based).  They may differ from the page numbers
printed in the document's own footer, because cover pages offset the numbering.  Cite
the rendered index.
"""
import argparse
import json
from pathlib import Path

import pymupdf


# Figures smaller than this (in pixels, either dimension) are almost always logos,
# bullets or rules rather than content worth reading.
MIN_FIGURE_PX = 120


def extract_figures(doc, page, page_no: int, outdir: Path) -> list[dict]:
    """Pull embedded images out at native resolution, one file each.

    Uses get_image_info(xrefs=True), which lists images actually *placed* on the page.
    page.get_images() lists the page's /Resources dict instead, and when a converted
    document shares one resource dict across pages that returns every figure in the
    document for every page -- which looks like it works right up until an agent reads
    the wrong figure for its problem.
    """
    figs = []
    seen = set()
    for info in page.get_image_info(xrefs=True):
        xref = info.get("xref", 0)
        if not xref or xref in seen:
            continue
        seen.add(xref)
        try:
            raw = doc.extract_image(xref)
        except Exception:
            continue
        w, h = raw.get("width", 0), raw.get("height", 0)
        if w < MIN_FIGURE_PX or h < MIN_FIGURE_PX:
            continue  # logo / rule / bullet
        name = f"page_{page_no:03d}_fig_{len(figs)+1:02d}.{raw['ext']}"
        (outdir / name).write_bytes(raw["image"])
        bbox = info.get("bbox")
        figs.append({"file": name, "width": w, "height": h,
                     "bbox_on_page": [round(v, 1) for v in bbox] if bbox else None})
    return figs


def render(pdf_path: Path, outdir: Path, dpi: int = 200):
    outdir.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(pdf_path)
    pages = []
    alltext = []
    for i, page in enumerate(doc, start=1):
        png = outdir / f"page_{i:03d}.png"
        txt = outdir / f"page_{i:03d}.txt"
        pix = page.get_pixmap(dpi=dpi)
        pix.save(png)
        text = page.get_text()
        txt.write_text(text)
        figs = extract_figures(doc, page, i, outdir)
        alltext.append(f"\n===== rendered page {i} =====\n{text}")
        pages.append({
            "rendered_page": i,
            "png": png.name,
            "txt": txt.name,
            "width": pix.width,
            "height": pix.height,
            "n_chars": len(text),
            "n_images": len(page.get_images()),
            "figures": figs,
        })
    (outdir / "alltext.txt").write_text("".join(alltext))
    manifest = {"source": str(pdf_path), "dpi": dpi,
                "n_pages": doc.page_count, "pages": pages}
    (outdir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return manifest


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--dpi", type=int, default=200)
    a = ap.parse_args()
    m = render(Path(a.pdf), Path(a.outdir), a.dpi)
    print(f"{m['n_pages']} pages -> {a.outdir}")
    for p in m["pages"]:
        print(f"  page {p['rendered_page']}: {p['n_chars']} chars, "
              f"{len(p['figures'])} figure(s) extracted at native resolution")
        for f in p["figures"]:
            print(f"      {f['file']}  ({f['width']}x{f['height']}) "
                  f"<-- READ THIS FILE for figure content, not the whole-page PNG")


if __name__ == "__main__":
    main()
