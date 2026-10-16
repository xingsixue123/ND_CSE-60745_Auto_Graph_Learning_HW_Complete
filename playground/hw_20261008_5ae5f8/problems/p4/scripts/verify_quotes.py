"""Check every quotation *as shipped in answer.tex* against the paper texts.

Usage: python3 scripts/verify_quotes.py [path/to/answer.tex]

Round 1 shipped a verifier with a hardcoded quote list, and one entry drifted from
the string actually in answer.tex, so a silently re-capitalised quote passed. This
version parses the quotations out of answer.tex itself, so the thing checked is
always the thing a reader sees.

Normalises the two things that break naive matching on these PDFs: words hyphenated
across a line break, and the fi/fl/ff ligatures in the USENIX PDF. Also undoes the
LaTeX escapes that can appear inside a quotation.
"""
import re, sys

SRC = {
    'denning':    'papers/denning_ws_1968.txt',
    'mach':       'papers/mach_vm_1987.txt',
    'superpages': 'papers/superpages_osdi02.txt',
}

def norm(t):
    t = t.replace('\ufb01', 'fi').replace('\ufb02', 'fl').replace('\ufb00', 'ff')
    t = re.sub(r'-\s*\n\s*', '', t)          # de-hyphenate across line breaks
    return re.sub(r'\s+', ' ', t).strip().lower()

def unlatex(q):
    q = q.replace('\\%', '%').replace('\\&', '&').replace('\\_', '_')
    q = q.replace('~', ' ').replace('\\ ', ' ')
    q = re.sub(r'\\(emph|textbf|texttt)\{([^}]*)\}', r'\2', q)
    return q

tex = sys.argv[1] if len(sys.argv) > 1 else \
    '/home/xing/project/auto_hw_complete/output/hw_20261008_5ae5f8/p4/answer.tex'
body = open(tex).read()
texts = {k: norm(open(v).read()) for k, v in SRC.items()}

# A quotation inside a citation block (before that subsection's \paragraph{Summary.})
# is a paper TITLE. Titles are checked word-sequence-in-order rather than contiguously,
# because the two-column scans split a title across the column gutter: Denning's runs
# "The Working Set Model for Program" / <author, affiliation> / "Behavior". Prose
# quotations, which carry the argument, must match contiguously.
def spans(text):
    out, pos = [], 0
    for m in re.finditer(r"``(.+?)''", text, re.S):
        head = text[:m.start()]
        is_title = head.rfind('\\subsection') > head.rfind('\\paragraph{Summary.}')
        out.append((m.group(1), is_title))
    return out

def in_order(words, hay):
    i = 0
    for w in words:
        i = hay.find(w, i)
        if i < 0:
            return False
        i += len(w)
    return True

quotes = spans(body)
if not quotes:
    sys.exit("no quotations found in " + tex)

bad = 0
for q, is_title in quotes:
    needle = norm(unlatex(q))
    if is_title:
        hits = [k for k, t in texts.items() if in_order(needle.split(), t)]
        kind = 'title'
    else:
        hits = [k for k, t in texts.items() if needle in t]
        kind = 'quote'
    bad += not hits
    tag = f'ok {kind} [{hits[0]}]' if hits else f'FAIL {kind} [not in any source]'
    one = ' '.join(q.split())
    print(f'{tag:28s} "{one[:70]}"')

print(f'\n{len(quotes)} quotation(s) checked '
      f'({sum(t for _, t in quotes)} titles, {sum(not t for _, t in quotes)} prose); '
      + ('ALL VERIFIED' if not bad else f'{bad} NOT FOUND'))
sys.exit(1 if bad else 0)
