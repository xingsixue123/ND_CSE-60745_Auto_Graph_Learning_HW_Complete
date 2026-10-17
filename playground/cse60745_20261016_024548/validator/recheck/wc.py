import re, sys
def prose(tex, drop_captions=True):
    t = tex
    t = re.sub(r'(?s)\\begin\{lstlisting\}.*?\\end\{lstlisting\}', ' ', t)
    t = re.sub(r'(?s)\\begin\{tabular\}.*?\\end\{tabular\}', ' ', t)
    t = re.sub(r'(?s)\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}', ' ', t)
    t = re.sub(r'(?s)\\lstdefinestyle\{.*?\n\}', ' ', t)
    caps = re.findall(r'\\caption\{', t)
    if drop_captions:
        # remove \caption{...} with brace matching
        out=[]; i=0
        while True:
            m=re.search(r'\\caption\{', t[i:])
            if not m: out.append(t[i:]); break
            s=i+m.start(); out.append(t[i:s]); j=s+len(m.group(0)); d=1
            while j<len(t) and d:
                if t[j]=='{': d+=1
                elif t[j]=='}': d-=1
                j+=1
            i=j
        t=''.join(out)
    t = re.sub(r'(?s)%.*?\n', ' ', t)
    t = re.sub(r'\$[^$]*\$', ' X ', t)
    t = re.sub(r'\\[a-zA-Z@]+\*?', ' ', t)
    t = re.sub(r'[{}\[\]&\\~^_]', ' ', t)
    return len([w for w in re.split(r'\s+', t) if re.search(r'[A-Za-z0-9]', w)]), len(caps)

for f in sys.argv[1:]:
    tex=open(f).read()
    # split by \section
    parts = re.split(r'\\section\*?\{', tex)
    print(f'=== {f} ===')
    n,c = prose(tex); print(f'  WHOLE FILE prose (no code/tables/captions): {n} words, {c} captions')
    nc,_ = prose(tex, drop_captions=False); print(f'  including captions: {nc} words')
    for p in parts[1:]:
        title=p.split('}')[0]
        n2,_=prose('{'+p)
        print(f'   section "{title}": {n2} prose words')
