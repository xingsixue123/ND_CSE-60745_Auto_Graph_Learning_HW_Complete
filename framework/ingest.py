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
sys.path.insert(0, str(Path(__file__).parent))
from tools.pdf_pages import render  # noqa: E402

OFFICE = {".doc", ".docx", ".odt", ".rtf", ".ppt", ".pptx", ".odp",
          ".xls", ".xlsx", ".ods"}
IMAGE = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff"}


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


def ingest(input_dir: Path, outdir: Path) -> dict:
    outdir.mkdir(parents=True, exist_ok=True)
    profile = outdir / ".loprofile"
    pdf_dir = outdir / "pdf"
    entries = []

    for src in sorted(input_dir.rglob("*")):
        if not src.is_file() or src.name.startswith("."):
            continue
        suf = src.suffix.lower()
        rec = {"source": str(src), "name": src.name, "kind": None,
               "bytes": src.stat().st_size}

        if suf == ".pdf":
            rec["kind"] = "document"
            pdf = src
        elif suf in OFFICE:
            rec["kind"] = "document"
            print(f"converting {src.name} -> pdf")
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
        man = render(Path(pdf), pages_dir, dpi=150)
        rec["pages_dir"] = str(pages_dir)
        rec["n_pages"] = man["n_pages"]
        rec["pages"] = man["pages"]
        entries.append(rec)
        print(f"  {src.name}: {man['n_pages']} pages -> {pages_dir}")

    manifest = {"input_dir": str(input_dir), "entries": entries}
    (outdir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--outdir", required=True)
    a = ap.parse_args()
    m = ingest(Path(a.input), Path(a.outdir))
    docs = [e for e in m["entries"] if e["kind"] == "document"]
    data = [e for e in m["entries"] if e["kind"] == "data"]
    print(f"\ningest complete: {len(docs)} document(s), {len(data)} data file(s)")
    for e in docs:
        imgs = sum(p["n_images"] for p in e.get("pages", []))
        print(f"  {e['name']}: {e.get('n_pages')} rendered pages, "
              f"{imgs} embedded images (READ THE PNGs, not just the text)")
    for e in data:
        print(f"  {e['name']}: {e.get('n_lines', '?')} lines")


if __name__ == "__main__":
    main()
