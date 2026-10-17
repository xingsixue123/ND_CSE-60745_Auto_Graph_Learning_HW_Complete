"""Prose word count of answer.tex per section, excluding listings, tables, captions, macros."""
import re
import sys

t = open(sys.argv[1] if len(sys.argv) > 1 else
         "/home/xing/project/auto_hw_complete/output/cse60745_20261016_024548/p1/answer.tex").read()
t = re.sub(r"\\begin\{lstlisting\}.*?\\end\{lstlisting\}", " ", t, flags=re.S)
t = re.sub(r"\\begin\{table\}.*?\\end\{table\}", " ", t, flags=re.S)
t = re.sub(r"\\lstdefinestyle\{.*?\n\}", " ", t, flags=re.S)
t = re.sub(r"^\s*\\definecolor.*$", " ", t, flags=re.M)
t = re.sub(r"^%.*$", " ", t, flags=re.M)
parts = re.split(r"\\section\{(.*?)\}", t)
for name, body in zip(parts[1::2], parts[2::2]):
    body = re.sub(r"\\subsection\*?\{.*?\}", " ", body)
    body = re.sub(r"\\texttt\{(.*?)\}", r"\1", body)
    body = re.sub(r"\$[^$]*\$", "x", body)
    body = re.sub(r"\\[a-zA-Z]+\*?", " ", body)
    body = re.sub(r"[{}\\~]", " ", body)
    print(f"{len(body.split()):5d} words  --  {name}")
