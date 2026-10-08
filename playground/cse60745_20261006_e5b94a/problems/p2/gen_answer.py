"""Builds OUTPUT/answer.tex and OUTPUT/preamble.txt.

The code listing is lifted out of run/rgcn_run.py by AST, and every number is read
back out of a run log, so the fragment cannot drift from the code that produced it.
"""
import ast, json, pathlib, re, statistics as st

HERE = pathlib.Path(__file__).parent
RUN = HERE / "run"
OUT = pathlib.Path("/home/xing/project/auto_hw_complete/output/cse60745_20261006_e5b94a/p2")

src = (RUN / "rgcn_run.py").read_text()
tree = ast.parse(src)
cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "MyRGCNConv")
code = ast.get_source_segment(src, cls).rstrip()

def result_of(p):
    return json.loads(re.search(r"RESULT_JSON (\{.*\})", pathlib.Path(p).read_text()).group(1))

res = result_of(RUN / "rgcn_run.log")                       # the authoritative run (= run 1)
runs = [result_of(RUN / f"rgcn_run_{i}.log") for i in range(1, 6)]
vm = [r["MRR"] for r in runs]
tm = [r["test_MRR"] for r in runs]
spread = f"${st.mean(vm):.3f}\\pm{st.pstdev(vm):.3f}$"
tspread = f"${st.mean(tm):.3f}\\pm{st.pstdev(tm):.3f}$"
print("authoritative (run 1):", res)
print("five processes, val  MRR:", [round(v, 4) for v in vm], "->", spread)
print("five processes, test MRR:", [round(v, 4) for v in tm], "->", tspread)

# cross-checks, read back from their own logs
cvp = (RUN / "check_vs_pyg.log").read_text()
pyg = json.loads(re.search(r"PYG_RESULT_JSON (\{.*\})", cvp).group(1))
agree = float(re.search(r"max \|mine - PyG RGCNConv\| = ([0-9.e+-]+)", cvp).group(1))
m, e = f"{agree:.0e}".split("e")
agree_tex = f"${m}\\times10^{{{int(e)}}}$"
print("agreement with RGCNConv:", agree, "->", agree_tex)
abl = (RUN / "ablation.log").read_text()
assert "|variant A - delivered layer| max = 0.000e+00" in abl, \
    "ablation control no longer reproduces the delivered layer"
scale = {m[0]: float(m[1]) for m in
         re.findall(r"relation \d (\w+)\s+mean (\d\.\d+)\s+median", abl)}
down = re.search(r"relation 0 friend\s+mean \d\.\d+\s+median \d\.\d+\s+"
                 r"\(= down-weighting by ([\d.]+)x\)", abl).group(1)
summ = {m[0]: float(m[1]) for m in
        re.findall(r"^([ABCD]) .*?\s+(\d\.\d{4})\s+\d\.\d{4}\s*$", abl, re.M)}
assert set(summ) == {"A", "B", "C", "D"}, f"ablation summary not fully parsed: {summ}"
assert abs(summ["A"] - st.mean(vm)) < 0.05, \
    f"ablation control {summ['A']} does not track the delivered five-run mean {st.mean(vm):.4f}" 
print("ablation scale factors:", scale, "| friend down-weighting:", down, "x")
print("ablation val MRR by variant:", summ)
d2 = (RUN / "diagnose2.log").read_text()
ci = [float(m) for m in re.findall(r"c_i seed\d+\s+val MRR (\d\.\d+)", d2)]
print("PyG RGCNConv val MRR:", round(pyg["MRR"], 4),
      "| diagnose2 pooled-c_i (independent process):", round(st.mean(ci), 4))

TEX = r"""\section{Q4: R-GCN Implementation}
\label{p2:sec:rgcn}

\definecolor{pTwoKw}{RGB}{0,92,197}
\definecolor{pTwoCmt}{RGB}{106,115,125}
\definecolor{pTwoStr}{RGB}{3,47,98}
\definecolor{pTwoRule}{RGB}{190,190,190}

\lstdefinestyle{pTwoPyStyle}{%
  language=Python,
  basicstyle=\ttfamily\footnotesize,
  keywordstyle=\color{pTwoKw}\bfseries,
  commentstyle=\color{pTwoCmt}\itshape,
  stringstyle=\color{pTwoStr},
  showstringspaces=false,
  columns=fullflexible,
  keepspaces=true,
  breaklines=true,
  breakautoindent=true,
  frame=single,
  rulecolor=\color{pTwoRule},
  framesep=4pt,
  xleftmargin=1.0em,
  numbers=none,
  tabsize=4,
}

\begin{lstlisting}[style=pTwoPyStyle]
__CODE__
\end{lstlisting}

\noindent
\texttt{self.rel[r]} is $W_r$: one full $\mathrm{in}\times\mathrm{out}$ matrix per
relation, with neither of the decompositions Schlichtkrull et al.\ add as
regularisers~--- the \emph{basic} version. \texttt{self.root} is $W_0$, applied
to $h_i$ outside any propagation.

I took $c_{i,r}=|N_r(i)|$, the example their Eq.~(2) offers, which is exactly
\texttt{aggr="mean"}. Guarding it is not optional: all 15{,}466 nodes have
$|N_r(i)|=0$ for some $r$; PyG's mean divides by \texttt{count.clamp(min=1)},
returning $0$ rather than NaN.

\texttt{edge\_type} never reaches \texttt{propagate}: \texttt{forward} slices
\texttt{edge\_index} by relation and propagates once per subset, so relation $r$'s
edges only meet $W_r$ and the stub's
\texttt{message(self,\,x\_j)} is untouched. $W_r$ is applied before propagating rather
than after~--- $c_{i,r}$ does not depend on $j$ and $W_r$ is linear, so
$\sum_{j} c_{i,r}^{-1} W_r h_j = W_r\!\left(\operatorname{mean}_{j} h_j\right)$~---
transforming 15{,}466 rows instead of 3{,}014{,}361 messages. \texttt{size=(n,\,n)}
keeps every relation's output at the full node count.

\medskip
\noindent
Cell 28's \texttt{train\_and\_eval\_hetero("R-GCN")}, run unmodified, selected
epoch~__EPOCH__:

\begin{center}
\begin{tabular}{lcc}
\toprule
 & MRR & Hit@1 \\
\midrule
validation & __VMRR__ & __VH1__ \\
test       & __TMRR__ & __TH1__ \\
\bottomrule
\end{tabular}
\end{center}

\noindent
Random tie-breaking over 21 candidates already scores MRR $0.174$, and training loss
settles at $\ln 2$ with the scores collapsed towards zero, so the model barely beats
chance. Cell 26's features come from gensim's \texttt{Word2Vec} at \texttt{workers=4},
not reproducible across processes; over five runs validation MRR was __SPREAD__
and test MRR __TSPREAD__, so read the table with that spread. The layer is not the cause:
\texttt{torch\_geometric.nn.RGCNConv} in the same harness scores __PYGMRR__, and my
\texttt{forward} matches it to __AGREE__ on all 6{,}067{,}650 edges. The normalisation is
the lever: pooling, as the paper's link-prediction experiments do
($c_{i,r}=c_i=\sum_r|N_r(i)|$), reaches $__POOLED__$~--- not by smoothing the dense
relations less, whose scale it barely changes ($\times__S1__$, $\times__S2__$), but by
dividing the sparse \texttt{friend} term, whose edges \emph{are} the training positives,
by __DOWN__. Pooling \texttt{friend} alone gives $__FRIENDONLY__$.
"""

tex = (TEX.replace("__CODE__", code)
          .replace("__EPOCH__", str(res["epoch"]))
          .replace("__VMRR__", f"{res['MRR']:.4f}")
          .replace("__VH1__", f"{res['hit@1']:.4f}")
          .replace("__TMRR__", f"{res['test_MRR']:.4f}")
          .replace("__TH1__", f"{res['test_hit@1']:.4f}")
          .replace("__SPREAD__", spread)
          .replace("__TSPREAD__", tspread)
          .replace("__AGREE__", agree_tex)
          .replace("__PYGMRR__", f"${pyg['MRR']:.3f}$")
          .replace("__POOLED__", f"{summ['B']:.3f}")
          .replace("__FRIENDONLY__", f"{summ['C']:.3f}")
          .replace("__S1__", f"{scale['listens']:.2f}")
          .replace("__S2__", f"{scale['listened_by']:.2f}")
          .replace("__DOWN__", f"${round(float(down))}$"))

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "answer.tex").write_text(tex)
(OUT / "preamble.txt").write_text(
    "\\usepackage{listings}\n\\usepackage{xcolor}\n\\usepackage{booktabs}\n"
    "\\usepackage{amsmath}\n")

# R8: count the PROSE only -- not the listing, not the table, not the lst/color setup
prose = re.sub(r"\\begin\{lstlisting\}.*?\\end\{lstlisting\}", " ", tex, flags=re.S)
prose = re.sub(r"\\begin\{center\}.*?\\end\{center\}", " ", prose, flags=re.S)
prose = re.sub(r"\\lstdefinestyle\{pTwoPyStyle\}\{%.*?\n\}", " ", prose, flags=re.S)
prose = re.sub(r"\\definecolor\{[^}]*\}\{[^}]*\}\{[^}]*\}", " ", prose)
prose = re.sub(r"\\section\{.*?\}|\\label\{.*?\}", " ", prose)
prose = re.sub(r"\$[^$]*\$", " x ", prose)
prose = re.sub(r"\\[a-zA-Z]+\*?", " ", prose)
prose = re.sub(r"[{}~^&%\\]", " ", prose)
words = [w for w in prose.split() if re.search(r"[A-Za-z0-9]", w)]
print("PROSE WORD COUNT:", len(words))
print("wrote", OUT / "answer.tex")
