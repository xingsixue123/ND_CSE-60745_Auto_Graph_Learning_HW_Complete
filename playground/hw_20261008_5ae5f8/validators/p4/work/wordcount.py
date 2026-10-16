import re,sys
src=open(sys.argv[1]).read()
# split into blocks by \subsection*
parts=re.split(r'\\subsection\*\{',src)
def clean(t):
    t=re.sub(r'\\(section|subsection|paragraph)\*?\{[^}]*\}',' ',t)
    t=re.sub(r'\\[a-zA-Z]+\*?','',t)      # commands
    t=re.sub(r'[{}$\\~^_]',' ',t)
    t=re.sub(r'``|\'\'',' ',t)
    return [w for w in re.split(r'\s+',t) if re.search(r'[A-Za-z0-9]',w)]
print('intro:',len(clean(parts[0])))
tot=len(clean(parts[0]))
for p in parts[1:]:
    head=p.split('}')[0]
    body=p[len(head)+1:]
    # citation = text before \paragraph{Summary
    i=body.find('\\paragraph{Summary.}')
    cit,rest=body[:i],body[i:]
    j=rest.find('\\paragraph{Critique.}')
    s,c=rest[:j],rest[j:]
    ls,lc=len(clean(s)),len(clean(c))
    print(f'{head[:40]:42s} cite={len(clean(cit)):4d} summary={ls:4d} critique={lc:4d} total={ls+lc:4d}  split={ls/(ls+lc):.0%}/{lc/(ls+lc):.0%}')
    tot+=ls+lc
print('BODY TOTAL (excl. citations/headings):',tot)
emd=src.count('---')
print('em-dashes:',emd,' -> one per',round(tot/max(emd,1)),'words')
