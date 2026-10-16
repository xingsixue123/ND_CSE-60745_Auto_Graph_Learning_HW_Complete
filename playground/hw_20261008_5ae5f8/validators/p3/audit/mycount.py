import re, sys
# Independent method: keep math CONTENT as words (worker collapsed each $..$ to 1 token),
# strip only comments, the tikz env, control sequences and grouping chars.
TARGETS = {"3.3":190,"3.4":190,"3.5":190,"3.6":190,"3.7":290,"3.8":330}
src = open(sys.argv[1]).read()
src = re.sub(r'(?<!\\)%.*', '', src)
src = re.sub(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}', ' ', src, flags=re.S)
# split on section headings, DROP the heading text itself
parts = re.split(r'\\section\*\{Ex\.\\?\s*(\d+\.\d+)[^}]*\}', src)
pairs = list(zip(parts[1::2], parts[2::2]))
def words(t):
    t = re.sub(r'\\begin\{[a-zA-Z*]+\}(\[[^\]]*\])?', ' ', t)
    t = re.sub(r'\\end\{[a-zA-Z*]+\}', ' ', t)
    t = re.sub(r'\\[a-zA-Z@]+\*?', ' ', t)   # control words
    t = re.sub(r'\\.', ' ', t)               # control symbols incl \ 
    t = t.replace('---',' ').replace('--',' ')
    t = re.sub(r"[{}\[\]$&~^_=<>|/\\]", ' ', t)
    toks = re.findall(r"[A-Za-z0-9''\-\.]+", t)
    return [w for w in toks if re.search(r'[A-Za-z0-9]', w) and w.strip('-.')]
tot=ttot=0
print(f"{'ex':>5} {'mine':>6} {'target':>7} {'ratio':>6}")
for n,b in pairs:
    w=len(words(b)); t=TARGETS[n]; tot+=w; ttot+=t
    print(f"{n:>5} {w:>6} {t:>7} {w/t:>5.2f}x")
print(f"{'TOT':>5} {tot:>6} {ttot:>7} {tot/ttot:>5.2f}x")
# raw sanity: total non-heading characters of prose
