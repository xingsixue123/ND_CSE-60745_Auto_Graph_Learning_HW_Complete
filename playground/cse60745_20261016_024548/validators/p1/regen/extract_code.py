"""Split solution.py into the three blocks that go into answer.tex, verbatim."""
import re

MARKERS = [("helpers", "# ===================== helpers ====================="),
           ("q1", "# ===================== notebook cell 13 - Q1 ====================="),
           ("q2", "# ===================== notebook cell 16 - Q2 =====================")]


def blocks(path="solution.py"):
    text = open(path).read()
    heads = [(m.group(1), m.start(), m.end()) for m in
             re.finditer(r"^# =+ (.*?) =+$", text, re.M)]
    out, names = {}, []
    for i, (title, s, e) in enumerate(heads):
        end = heads[i + 1][1] if i + 1 < len(heads) else len(text)
        names.append(title)
        out[title] = text[e:end].strip("\n")
    return out, names


if __name__ == "__main__":
    b, names = blocks()
    for n in names:
        print(f"--- {n}: {len(b[n].splitlines())} lines")
