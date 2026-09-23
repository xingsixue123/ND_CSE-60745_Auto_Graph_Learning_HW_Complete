import re, sys, unicodedata

def norm(p):
    t = open(p, encoding='utf-8', errors='replace').read()
    t = unicodedata.normalize('NFKD', t)
    t = t.replace('\u2019', "'").replace('\u2018', "'")
    t = t.replace('\u201c', '"').replace('\u201d', '"')
    t = t.replace('\u2013', '-').replace('\u2014', '-').replace('\u2212', '-')
    t = t.replace('\ufb01', 'fi').replace('\ufb02', 'fl')
    t = re.sub(r'-\n\s*', '', t)      # undo end-of-line hyphenation
    t = re.sub(r'\s+', ' ', t)
    return t

L = norm('mypapers/lottery.flow.txt')
S = norm('mypapers/stride.flow.txt')
B = norm('mypapers/buttazzo.flow.txt')
DOC = {'L': L, 'S': S, 'B': B}

CHECKS = [
 # (paper, needle, label)
 ('L', 'time scale of milliseconds to seconds', 'intro timescale quote'),
 ('L', 'time scale of minutes', 'fair-share related-work quote'),
 ('L', 'converge toward their allocated values over longer time intervals', 'convergence hedge'),
 ('L', '25378', 'dhrystone 2:1 winner iters'),
 ('L', '12619', 'dhrystone 2:1 loser iters'),
 ('L', '13.42', '10:1 observed ratio'),
 ('L', '19.08', '20:1 three-minute average'),
 ('L', '17.19', 'db response time 1'),
 ('L', '43.19', 'db response time 2'),
 ('L', '132.20', 'db response time 3'),
 ('L', '2.7%', 'overhead 3 dhrystone'),
 ('L', '0.8%', 'overhead 8 dhrystone'),
 ('L', '1.7%', 'db faster'),
 ('L', 'does not pose any challenging problems', 'efficiency conclusion quote'),
 ('L', 'setuid', 'setuid root commands'),
 ('L', 'Mach 3.0', 'prototype kernel'),
 ('L', 'DECStation', 'hardware'),
 ('L', '100 millisecond', 'quantum'),
 ('L', 'compensation ticket', 'compensation tickets'),
 ('L', 'exchange rate', 'currency exchange rate'),
 # stride
 ('S', 'VirtualClock', 'virtualclock rediscovery'),
 ('S', 'conceptually simpler', 'lottery simpler concession'),
 ('S', 'effectively stateless', 'stateless concession'),
 ('S', 'consistently lower than specified', 'ttcp delay constant quote'),
 ('S', 'ttcp', 'ttcp'),
 ('S', '3.001', 'cpu 3:1 measured'),
 ('S', '2409.18', 'cpu iters high'),
 ('S', '802.89', 'cpu iters low'),
 ('S', '1.1.50', 'linux version'),
 ('S', '300 lines', 'prototype size'),
 ('S', '19.64', 'lottery sigma fig12'),
 ('S', '194', 'lottery max range fig12'),
 # buttazzo
 ('B', '256', 'priority levels'),
 ('B', 'does not prove that EDF always introduces less jitter', 'jitter disclaimer'),
 ('B', 'highly application dependent', 'overload concession'),
 ('B', 'not very well suited', 'both unsuited to overload'),
 ('B', 'Constant Bandwidth Server', 'CBS'),
]

fails = []
for pap, needle, label in CHECKS:
    n = unicodedata.normalize('NFKD', needle)
    ok = n in DOC[pap]
    if not ok:
        # try whitespace-insensitive regex
        pat = re.compile(r'\s*'.join(re.escape(c) for c in n.replace(' ', '')), re.I)
        ok = bool(pat.search(DOC[pap]))
    print(('OK  ' if ok else 'FAIL'), pap, '|', label, '|', repr(needle))
    if not ok:
        fails.append((pap, needle, label))

print('\n%d/%d verified' % (len(CHECKS) - len(fails), len(CHECKS)))
sys.exit(1 if fails else 0)
