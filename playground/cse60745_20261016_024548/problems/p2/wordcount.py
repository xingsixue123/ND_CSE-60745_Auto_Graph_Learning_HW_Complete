"""Count prose words in a LaTeX fragment: math, commands, listings, tables and captions out."""
import re, sys
t = open(sys.argv[1]).read()
t = re.sub(r"\\begin\{lstlisting\}.*?\\end\{lstlisting\}", " ", t, flags=re.S)
t = re.sub(r"\\begin\{table\}.*?\\end\{table\}", " ", t, flags=re.S)
t = re.sub(r"\\begin\{figure\}.*?\\end\{figure\}", " ", t, flags=re.S)
t = re.sub(r"\\lstdefinestyle\{.*?\n\}", " ", t, flags=re.S)
t = re.sub(r"\$[^$]*\$", " ", t)                       # inline math
t = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", t)     # commands
t = re.sub(r"[{}~^_&\\]", " ", t)
words = [w for w in t.split() if re.search(r"[A-Za-z]", w)]
print(f"{sys.argv[1]}: {len(words)} prose words")
