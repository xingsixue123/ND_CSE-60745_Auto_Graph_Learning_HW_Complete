"""Strip HTML to a tab-delimited text dump so dataset stat tables stay row-aligned."""
import re, html, sys

for f in sys.argv[1:]:
    s = open(f, encoding='utf-8', errors='replace').read()
    s = re.sub(r'(?is)<(script|style).*?</\1>', ' ', s)
    s = re.sub(r'(?i)</(tr|p|div|h[1-6]|li)>', '\n', s)
    s = re.sub(r'(?i)</t[dh]>', '\t', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html.unescape(s)
    s = s.replace('\u00a0', ' ')
    s = re.sub(r'[ ]{2,}', ' ', s)
    s = '\n'.join(l.strip() for l in s.split('\n') if l.strip())
    out = f.replace('.html', '.txt')
    open(out, 'w').write(s)
    print(f, '->', out, len(s), 'chars')
