"""Re-check every quotation in answer.tex against the extracted paper text.

Usage: python3 scripts/verify_quotes.py
Normalises the two things that break naive grep on these PDFs: words hyphenated
across a line break, and the fi/fl/ff ligatures in the USENIX PDF.
"""
import re, sys

def norm(t):
    t = t.replace('ﬁ', 'fi').replace('ﬂ', 'fl').replace('ﬀ', 'ff')
    t = re.sub(r'-\s*\n\s*', '', t)      # de-hyphenate across line breaks
    return re.sub(r'\s+', ' ', t).lower()

SRC = {
    'denning':    '/home/xing/project/auto_hw_complete/playground/hw_20261008_5ae5f8/problems/p4/papers/denning_ws_1968.txt',
    'mach':       '/home/xing/project/auto_hw_complete/playground/hw_20261008_5ae5f8/problems/p4/papers/mach_vm_1987.txt',
    'superpages': '/home/xing/project/auto_hw_complete/playground/hw_20261008_5ae5f8/problems/p4/papers/superpages_osdi02.txt',
}
TEXT = {k: norm(open(v).read()) for k, v in SRC.items()}

QUOTES = [
    ('denning', 'references to the same page tend to cluster in time'),
    ('denning', 'Random brings on the highest page traffic, working set the lowest'),
    ('denning', 'is more than offset by its accuracy'),
    ('mach',    'about the size of a device driver'),
    ('mach',    'rare enough in normal application programs'),
    ('mach',    'sometimes occur during periods of heavy paging and cannot always be '
                'detected on the basis of in memory data structures alone'),
    ('superpages', 'may deny the benefits of superpages to processes that do not write '
                   'to all of the base pages'),
    ('superpages', 'these benefits are sustained even under stressful workload scenarios'),
]

bad = 0
for src, q in QUOTES:
    ok = norm(q) in TEXT[src]
    bad += not ok
    print(('ok   ' if ok else 'FAIL ') + f'[{src}] {q[:78]}')
print(('ALL QUOTATIONS VERIFIED' if not bad else f'{bad} QUOTATION(S) NOT FOUND'))
sys.exit(1 if bad else 0)
