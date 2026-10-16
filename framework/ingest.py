#!/usr/bin/env python3
"""Normalize whatever the user dropped in input/ into something agents can read.

Every document (.doc .docx .odt .rtf .ppt .pptx .xls .xlsx) is converted to PDF with
headless LibreOffice, then every PDF is rendered to per-page PNGs plus per-page text
by pdf_pages.py.  Data files are left alone and simply catalogued.

This exists because the machine has no poppler and no Word converter of its own, and
because legacy .doc homework carries its figures as embedded images that pure text
extraction silently drops.

    python3 ingest.py --input <dir> --outdir <dir>
"""
import argparse
import json
import shutil
import subprocess
from pathlib import Path

import sys

import pymupdf

sys.path.insert(0, str(Path(__file__).parent))
from tools.pdf_pages import render  # noqa: E402


def text_only(pdf_path: Path, outdir: Path) -> dict:
    """Extract text without rendering images -- for material over the render budget."""
    outdir.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(pdf_path)
    alltext, pages = [], []
    for i, page in enumerate(doc, start=1):
        text = page.get_text()
        (outdir / f"page_{i:03d}.txt").write_text(text)
        alltext.append(f"\n===== rendered page {i} =====\n{text}")
        pages.append({"rendered_page": i, "txt": f"page_{i:03d}.txt",
                      "n_chars": len(text),
                      "n_vector_drawings": len(page.get_drawings()),
                      "figures": []})
    (outdir / "alltext.txt").write_text("".join(alltext))
    return {"source": str(pdf_path), "n_pages": doc.page_count, "pages": pages}

OFFICE = {".doc", ".docx", ".odt", ".rtf", ".ppt", ".pptx", ".odp",
          ".xls", ".xlsx", ".ods"}
# A spreadsheet rendered to PDF extracts column-major -- every ID, then every title,
# then every category -- so the rows come apart and values get mis-associated.  Also
# emit CSV, which keeps rows intact.
SPREADSHEET = {".xls", ".xlsx", ".ods", ".csv"}
IMAGE = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff"}
# An assignment is not always a PDF.  A markdown or plain-text assignment has no
# pages and no figures, so there is nothing to render -- but it is still the
# assignment, and classifying it as a data file buries it among the real data.
TEXT_DOC = {".md", ".txt", ".rst", ".org", ".tex", ".ipynb"}

# Rendering every page of every input does not scale: a course that ships 300 pages
# of lecture slides alongside a two-page assignment would spend minutes and ~100 MB
# rendering material the assignment may never refer to.  Pages are rendered until
# this budget is spent, assignment files first; whatever is left keeps its extracted
# text and can be rendered on demand with `pdf_pages.py --page N`.
RENDER_BUDGET_PAGES = 80


def to_pdf(src: Path, outdir: Path, profile: Path) -> Path | None:
    soffice = shutil.which("soffice")
    if not soffice:
        raise RuntimeError("soffice not found; cannot convert %s" % src.name)
    outdir.mkdir(parents=True, exist_ok=True)
    profile.mkdir(parents=True, exist_ok=True)
    # -env:UserInstallation must point somewhere writable or LibreOffice tries $HOME
    # and dies inside the sandbox.
    proc = subprocess.run(
        [soffice, "--headless", "--norestore",
         f"-env:UserInstallation=file://{profile}",
         "--convert-to", "pdf", "--outdir", str(outdir), str(src)],
        capture_output=True, text=True, timeout=600)
    pdf = outdir / (src.stem + ".pdf")
    if not pdf.is_file():
        print(f"  !! conversion failed for {src.name}: {proc.stdout}{proc.stderr}")
        return None
    return pdf


def notebook_to_text(src: Path) -> str:
    """Flatten a .ipynb to its cells in order: markdown as prose, code as code.

    Outputs are dropped. They are the previous author's results, and an agent that
    reads them may report them as its own rather than running the code itself.
    """
    import json as _json
    try:
        nb = _json.loads(src.read_text(errors="replace"))
    except Exception as exc:
        return f"(could not parse {src.name} as a notebook: {exc})"
    out = []
    for i, cell in enumerate(nb.get("cells", []), start=1):
        kind = cell.get("cell_type", "?")
        body = "".join(cell.get("source", []))
        out.append(f"\n===== cell {i} ({kind}) =====\n{body}")
    return "".join(out)


def to_csv(src: Path, outdir: Path, profile: Path) -> Path | None:
    """Export a spreadsheet to CSV so row structure survives."""
    soffice = shutil.which("soffice")
    if not soffice:
        return None
    outdir.mkdir(parents=True, exist_ok=True)
    profile.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [soffice, "--headless", "--norestore",
         f"-env:UserInstallation=file://{profile}",
         "--convert-to", "csv", "--outdir", str(outdir), str(src)],
        capture_output=True, text=True, timeout=600)
    csv = outdir / (src.stem + ".csv")
    return csv if csv.is_file() else None


def ingest(input_dir: Path, outdir: Path,
           budget: int = RENDER_BUDGET_PAGES) -> dict:
    outdir.mkdir(parents=True, exist_ok=True)
    profile = outdir / ".loprofile"
    pdf_dir = outdir / "pdf"
    entries = []

    # Files sitting directly in input/ are the assignment; anything in a
    # subdirectory (slides/, references/, data/) is supporting material.  Render the
    # assignment first so the budget is never spent on background reading.
    def rank(p: Path):
        return (len(p.relative_to(input_dir).parts) > 1, str(p))

    files = sorted((f for f in input_dir.rglob("*")
                    if f.is_file() and not f.name.startswith(".")), key=rank)
    remaining = budget

    for src in files:
        suf = src.suffix.lower()
        rel = src.relative_to(input_dir)
        rec = {"source": str(src), "name": src.name,
               "relative_path": str(rel),
               "role": "assignment" if len(rel.parts) == 1 else "supporting",
               "kind": None, "bytes": src.stat().st_size}

        if suf in TEXT_DOC:
            rec["kind"] = "text_document"
            pages_dir = outdir / "pages" / src.stem
            pages_dir.mkdir(parents=True, exist_ok=True)
            if suf == ".ipynb":
                # A notebook is JSON. Dumped raw it reads as metadata, and an
                # assignment whose specification lives in its markdown cells looks
                # like a data file. Flatten it to the cells in order instead.
                text = notebook_to_text(src)
                rec["n_cells"] = text.count("\n===== cell ")
            else:
                text = src.read_text(errors="replace")
            (pages_dir / "alltext.txt").write_text(text)
            rec["pages_dir"] = str(pages_dir)
            rec["n_chars"] = len(text)
            entries.append(rec)
            extra = (f", {rec['n_cells']} cells" if "n_cells" in rec else "")
            print(f"  {src.name}: text document, {len(text)} chars{extra} "
                  f"(no rendering needed)")
            continue

        if suf == ".pdf":
            rec["kind"] = "document"
            pdf = src
        elif suf in OFFICE:
            rec["kind"] = "document"
            print(f"converting {src.name} -> pdf")
            if suf in SPREADSHEET:
                csv = to_csv(src, outdir / "csv", profile)
                if csv:
                    rec["csv"] = str(csv)
                    print(f"  {src.name}: also exported to {csv.name} "
                          f"(rows intact -- prefer this over the PDF text)")
            pdf = to_pdf(src, pdf_dir, profile)
            if pdf is None:
                rec["kind"] = "unconvertible"
                entries.append(rec)
                continue
            rec["converted_pdf"] = str(pdf)
        elif suf in IMAGE:
            rec["kind"] = "image"
            entries.append(rec)
            continue
        else:
            rec["kind"] = "data"
            with open(src, "rb") as fh:
                head = fh.read(2000)
            try:
                rec["head"] = head.decode("utf-8", "replace")[:600]
                rec["n_lines"] = sum(1 for _ in open(src, "rb"))
            except Exception:
                rec["head"] = "<binary>"
            entries.append(rec)
            continue

        pages_dir = outdir / "pages" / src.stem
        n_pages = pymupdf.open(pdf).page_count
        # Supporting material is never pre-rendered.  It is background reading the
        # assignment may or may not refer to; rendering hundreds of lecture slides
        # to answer eight short questions is waste, and it buries the assignment in
        # the manifest.  Its text is extracted, and any page can be rendered on
        # demand once an agent knows it needs that page.
        if rec["role"] == "assignment" and n_pages <= remaining:
            man = render(Path(pdf), pages_dir, dpi=200)
            rec["rendered"] = True
            rec["pages"] = man["pages"]
            remaining -= n_pages
            print(f"  {src.name}: {n_pages} pages rendered -> {pages_dir}")
        else:
            man = text_only(Path(pdf), pages_dir)
            rec["rendered"] = False
            why = ("supporting material" if rec["role"] != "assignment"
                   else "over the render budget")
            rec["render_hint"] = (
                f"Not pre-rendered ({why}). Text is extracted. To see a page: "
                f"python3 framework/tools/pdf_pages.py '{pdf}' --page N --dpi 200 "
                f"--out <file.png>")
            print(f"  {src.name}: {n_pages} pages, text only "
                  f"(over render budget; render on demand)")
        rec["pages_dir"] = str(pages_dir)
        rec["n_pages"] = n_pages
        entries.append(rec)

    manifest = {"input_dir": str(input_dir), "entries": entries}
    (outdir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--outdir", required=True)
    a = ap.parse_args()
    m = ingest(Path(a.input), Path(a.outdir))
    by = lambda k, r=None: [e for e in m["entries"]
                            if e["kind"] == k and (r is None or e.get("role") == r)]
    print("\ningest complete\n")
    print("ASSIGNMENT (files directly in input/):")
    for e in m["entries"]:
        if e.get("role") != "assignment":
            continue
        if e["kind"] == "text_document":
            print(f"  {e['name']}: text document, {e['n_chars']} chars")
        elif e["kind"] == "document":
            imgs = sum(p.get("n_images", 0) for p in e.get("pages", []))
            state = "rendered" if e.get("rendered") else "TEXT ONLY"
            print(f"  {e['name']}: {e.get('n_pages')} pages, {state}, "
                  f"{imgs} embedded images")
        elif e["kind"] == "data":
            print(f"  {e['name']}: data, {e.get('n_lines', '?')} lines")
        else:
            print(f"  {e['name']}: {e['kind']}")
    sup = [e for e in m["entries"] if e.get("role") == "supporting"]
    if sup:
        print("\nSUPPORTING MATERIAL (in subdirectories -- background reading, not "
              "the questions):")
        for e in sup:
            state = "rendered" if e.get("rendered") else "text only, render on demand"
            print(f"  {e['relative_path']}: {e.get('n_pages', '?')} pages, {state}")


if __name__ == "__main__":
    main()
