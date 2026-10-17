"""Build OUTPUT/answer.tex: prose template + the final code spliced verbatim from
solution.py + every table row read back from the result JSONs in logs/.

  ../../.venv-gt/bin/python build_answer.py
"""
import json
import os
import re

from extract_code import blocks

SUBMITTED = "2-hop ball+virtual"       # the strategy SparseSPDAttention itself uses

OUT = "build/dry/out"

code, names = blocks()
HELPERS, Q1CODE, Q2CODE = (code[n] for n in names)

q1 = json.load(open("build/dry/logs/zinc_q1_results.json"))
q2 = json.load(open("build/dry/logs/zinc_q2_results.json"))
abl = json.load(open("build/dry/logs/zinc_ablation_results.json"))
counts = json.load(open("build/dry/logs/zinc_pair_counts.json"))
lastfm = json.load(open("build/dry/logs/lastfm_results.json"))
lf = json.load(open("build/dry/logs/lastfm_final_results.json"))
rep = json.load(open("build/dry/logs/zinc_cell18_results.json"))["repeats"]
bench = {}
for line in open("build/dry/logs/lastfm_timing2.log"):
    m = re.match(r"^(\S.*?)\s{2,}pairs attended\s+([\d,]+) \| one step\s+([\d.]+)s", line)
    if m:
        bench[m.group(1).strip()] = (int(m.group(2).replace(",", "")), float(m.group(3)))

TEX = r"""
% --- listing style for problem p1 (namespaced) ---
\definecolor{p1kw}{RGB}{0,80,160}
\definecolor{p1cm}{RGB}{110,110,110}
\definecolor{p1st}{RGB}{160,60,20}
\lstdefinestyle{p1py}{%
  language=Python,
  basicstyle=\ttfamily\scriptsize,
  keywordstyle=\color{p1kw}\bfseries,
  commentstyle=\color{p1cm}\itshape,
  stringstyle=\color{p1st},
  showstringspaces=false,
  breaklines=true, breakatwhitespace=true, breakindent=2em,
  columns=fullflexible, keepspaces=true,
  xleftmargin=0.6em, aboveskip=0.8em, belowskip=0.4em,
}
\section{Q1: Structural Encoding in Graph Transformer}

\texttt{LapPETransformer} adds Laplacian eigenvector positions to every node once, before the
first block; \texttt{SPDAttention} adds a learnable per-head scalar, indexed by the pair's hop
distance, to every attention score. Two choices in the absolute encoding matter.

\textbf{Which eigenvectors, and at what scale.} The smallest eigenvalue of
$L = I - D^{-1/2} A D^{-1/2}$ is $0$ with the constant eigenvector $D^{1/2}\mathbf{1}$, the same
for every connected graph, so \texttt{precompute} drops it and returns columns
$1,\dots,\texttt{LAP\_K}$; a graph with fewer is zero-padded (ZINC's smallest molecule has $9$
nodes, so exactly $8$ exist). Each column is then scaled by $\sqrt{n}$:
eigenvector entries are $O(n^{-1/2})$, so unscaled a channel has RMS $0.011$ on the $7624$-node
LastFM graph, where \texttt{num\_atom\_types=0} leaves the encoding as the model's only input.

\textbf{Sign ambiguity.} $v$ and $-v$ are the same eigenvector and the solver picks one
arbitrarily, so each graph's channels get an independent random sign flip while training and the
identity at evaluation. That is an augmentation \emph{across} graphs, so it is skipped when the
batch holds only one --- on LastFM it would be noise on the model's only input.

The relative encoding computes all-pairs hop distances by frontier expansion: exact on ZINC,
blocked and stopped after \texttt{max\_dist} hops for LastFM's $7624 \times 7624$ matrix, which
costs nothing because every distance from \texttt{max\_dist} upwards shares one bias;
unreachable pairs keep their own row. The lookup is added to the scores before mask and softmax,
$\mathrm{score}_{ij} = q_i^\top k_j/\sqrt{d} + b_{\mathrm{SPD}(i,j)}$, which is Graphormer's
form. The distances were checked against a plain BFS, the eigenvectors against the dense
spectrum of $L$.

%%ZINC_Q1_TABLE%%

%%Q1_RESULT_PROSE%%

\subsection*{Implementation (notebook cell 13, with its two helpers)}

\begin{lstlisting}[style=p1py]
%%HELPERS%%
\end{lstlisting}

\begin{lstlisting}[style=p1py]
%%Q1CODE%%
\end{lstlisting}

\section{Q2: Efficient Graph Transformer}

\texttt{SparseSPDAttention} keeps Q1's parameters and \texttt{precompute} and changes only which
pairs exist. Five pair sets were built and compared (Table~\ref{p1:tab:q2}): the graph's edges
alone; plus one global virtual node; plus Exphormer's random expander at two widths; and the
2-hop ball --- every ordered pair at most two hops apart --- plus the virtual node. The
submitted class attends to the last of these, picked on validation. Its cost is
$\sum_v \deg(v)^2$ rather than $n^2$: %%BALL_ZINC%% pairs per ZINC molecule, %%BALL_LASTFM%%
on LastFM ($1.4\%$ of full). The expander was the a-priori favourite --- it alone keeps the
pair count $O(n)$ while mixing in $O(\log n)$ hops --- but both widths finished last on both
datasets.

\texttt{forward} gathers $q,k,v$ at the endpoints of each pair, adds the inherited SPD bias plus
one learnable bias per pair type, normalises with \texttt{segment\_softmax} over the pairs that
share a querying node, and scatters the weighted values back with \texttt{index\_\allowbreak{}add\_}. The
handout points at a \texttt{segment\_\allowbreak{}attention} helper that does not exist in PyG 2.8.1; cell 3
imports \texttt{softmax as\allowbreak{} segment\_\allowbreak{}softmax}, and that is what is used. The framework also
reports \texttt{enc["spd"]}$=0$ for pairs touching a virtual node, which would alias them with
genuine distance-$0$ self loops, so those go to the unreachable row of \texttt{spd\_table}
instead. On a complete pair set this path reproduces the dense Q1 attention to
$7.5\times10^{-8}$.

%%ZINC_Q2_TABLE%%

%%Q2_RESULT_PROSE%%

%%LASTFM_TABLE%%

\subsection*{Implementation (notebook cell 16)}

\begin{lstlisting}[style=p1py]
%%Q2CODE%%
\end{lstlisting}
"""


def esc(s):
    return s.replace("_", r"\_").replace("%", r"\%").replace("+", r"$+$")


# ---------- table 1 ----------
Q1ROWS = [("none: plain attention", "none (plain \\texttt{Attention})"),
          ("demo: centrality + CN", "demo: degree centrality $+$ common neighbours"),
          ("LapPE only", "LapPE only (absolute)"),
          ("SPD only", "SPD only (relative)"),
          ("LapPE + SPD (cell 14)", "\\textbf{LapPE $+$ SPD} (cell 14)")]
rows = []
for key, label in Q1ROWS:
    r = q1[key]
    bold = key.startswith("LapPE + SPD")
    f = (lambda x: "\\textbf{%s}" % x) if bold else (lambda x: x)
    rows.append(f"{label} & {f('%.4f' % r['val'])} & {f('%.4f' % r['test'])} & {r['epoch']} \\\\")
t1 = ("\\begin{table}[H]\n\\centering\n\\caption{}\n\\begin{tabular}{lccc}\n\\toprule\n"
      "encoding & val MAE & test MAE & best epoch \\\\\n\\midrule\n"
      + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}\n\\end{table}")
t1 = t1.replace("\\caption{}", "\\caption{ZINC subset, 30 epochs, dense attention; "
                "4 blocks, dim 64, 4 heads, the framework's fixed seed. "
                "Epoch selected on validation MAE.}\n\\label{p1:tab:q1}")

# ---------- table 2 ----------
REPEATS = ", ".join(f"{r['test']:.4f}" for r in rep)
seeds = {sd: json.load(open(f"build/dry/logs/zinc_seed{sd}_results.json")) for sd in (1, 2)}


def three_seeds(key_sparse, key_seed0_value):
    """mean and half-range of test MAE over the framework seed 0 and seeds 1 and 2."""
    vals = [key_seed0_value] + [seeds[sd][key_sparse]["test"] for sd in (1, 2)]
    return sum(vals) / 3, (max(vals) - min(vals)) / 2


Q2ROWS = [("local", "self loops $+$ graph edges"),
          ("local+virtual", "$+$ virtual node"),
          ("2-hop ball+virtual", "\\textbf{2-hop ball $+$ virtual} (submitted)"),
          ("local+expander+virtual", "$+$ 4-regular expander"),
          ("local+expander8+virtual", "$+$ 8-regular expander")]
rows = []
for key, label in Q2ROWS:
    r, c = q2[f"sparse: {key}"], counts[key]
    bold = key == SUBMITTED
    f = (lambda x: "\\textbf{%s}" % x) if bold else (lambda x: x)
    m, hr = three_seeds(f"sparse: {key}", r["test"])
    rows.append(f"{label} & {c['pairs']:.0f} & {100 * c['pairs'] / c['full']:.0f}\\% & "
                f"{f('%.4f' % r['val'])} & {f('%.4f' % r['test'])} & {m:.4f} $\\pm$ {hr:.4f} \\\\")
full = q1["LapPE + SPD (cell 14)"]
fm, fhr = three_seeds("full attention", full["test"])
rows.append("\\midrule\nfull attention (Q1) & %.0f & 100\\%% & %.4f & %.4f & %.4f $\\pm$ %.4f \\\\"
            % (counts["local"]["full"], full["val"], full["test"], fm, fhr))
t2 = ("\\begin{table}[H]\n\\centering\n\\caption{Masking strategies on ZINC, same model and "
      "budget as Table~\\ref{p1:tab:q1}, with LapPE throughout. Pairs are per graph, averaged "
      "over the 10{,}000 training molecules ($n^2 = 557$ on average). The val and test columns "
      "are the framework's seed, as cell 18 runs it; the last column is the mean and half-range "
      "of the test MAE over that seed and two more, the expander rows redrawing their expander "
      "each time. Re-running the submitted row three times with every input identical --- same "
      "seed, same weights, same batch order --- gives test MAE " + REPEATS + ": the sparse "
      "forward accumulates with \\texttt{index\\_add\\_}, whose order across CPU threads is not "
      "fixed, so one ZINC number here is good to about $\\pm$0.01. All of this compares pair "
      "sets inside this framework --- 30 epochs, and the bond features \\texttt{make\\_batch} "
      "carries are never read --- rather than reproducing any paper's numbers.}\n"
      "\\label{p1:tab:q2}\n\\small\n\\begin{tabular}{lrrccc}\n\\toprule\n"
      "attention pairs & pairs/graph & of full & val MAE & test MAE & 3-seed mean \\\\\n\\midrule\n"
      + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}\n\\end{table}")

# ---------- table 3 ----------
BROWS = [("full: LapPE + SPD", "full attention (Q1)"),
         ("sparse: local", "self loops $+$ graph edges"),
         ("sparse: local+virtual", "$+$ virtual node"),
         ("sparse: 2-hop ball+virtual", "2-hop ball $+$ virtual"),
         ("sparse: local+expander+virtual", "$+$ 4-regular expander"),
         ("sparse: local+expander8+virtual", "$+$ 8-regular expander")]
rows = []
for key, label in BROWS:
    p_, sec = bench[key]
    f1 = lf
    name = key.replace("sparse: ", "")
    acc = f"{f1[name]['test']:.4f}" if name in f1 else "---"
    if name == SUBMITTED:
        label, acc = "\\textbf{%s} (submitted)" % label, "\\textbf{%s}" % acc
    rows.append((f"{label} & {p_:,} & {100 * p_ / 7624 ** 2:.3f}\\% & {sec:.2f} & {acc} \\\\"
                 ).replace(",", "{,}"))
cap3 = ("LastFM (7624 nodes, 27{,}806 edges, 18 countries), 2 blocks, dim 32, 2 heads, CPU, "
        "8 threads. One training step is the best of 7 forward-backward passes; micro-F1 is "
        "\\texttt{run\\_node\\_task} over 200 epochs, selected on validation. Full attention is "
        "not trained for 200 epochs: at %.2f\\,s a step it would cost more than every other "
        "experiment here together. The framework's peak-memory column prints "
        "\\texttt{n/a on CPU}, so no memory figure is quoted." % bench["full: LapPE + SPD"][1])
t3 = ("\\begin{table}[H]\n\\centering\n\\caption{" + cap3 + "}\n"
      "\\label{p1:tab:q2lastfm}\n\\small\n\\begin{tabular}{lrrrc}\n\\toprule\n"
      "attention pairs & pairs attended & of full & one step (s) & test micro-F1 \\\\\n"
      "\\midrule\n" + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}\n\\end{table}")

# ---------- derived prose ----------
spd_only, base = q1["SPD only"], q1["LapPE + SPD (cell 14)"]
a1, a2 = abl["ablation: no sqrt(n) scaling"], abl["ablation: no sign flip"]
lff = lf
q1prose = (
    "Both encodings help and SPD carries almost all of it: plain attention is at %.4f test MAE, "
    "SPD alone at %.4f, LapPE alone at %.4f. Putting LapPE on top of SPD moves it by %.4f, "
    "inside the $\\pm$%.4f seed-to-seed half-range Table~\\ref{p1:tab:q2} measures for that same "
    "model, so this budget does not establish a LapPE effect beyond SPD. Both choices above were "
    "ablated on both datasets, and they behave differently. The $\\sqrt{n}$ scaling is invisible "
    "on ZINC (%.4f against %.4f) and worth %.4f micro-F1 on LastFM. The sign flip is worth %.4f "
    "test MAE on ZINC and costs %.4f micro-F1 on LastFM, which is why it is conditional."
) % (q1["none: plain attention"]["test"], spd_only["test"], q1["LapPE only"]["test"],
     spd_only["test"] - base["test"], fhr,
     a1["test"], base["test"],
     lff[SUBMITTED]["test"] - lff["ablation: no sqrt(n) scaling"]["test"],
     a2["test"] - base["test"],
     lff[SUBMITTED]["test"] - lff["ablation: sign flip forced on"]["test"])

STRAT_KEYS = ["local", "local+virtual", "2-hop ball+virtual",
              "local+expander+virtual", "local+expander8+virtual"]


def mean3(name):
    return three_seeds(f"sparse: {name}", q2[f"sparse: {name}"]["test"])[0]


best_val = min(((k, v) for k, v in q2.items()), key=lambda kv: kv[1]["val"])[0]
assert best_val == f"sparse: {SUBMITTED}", best_val          # ZINC picks the submitted pair set
lf_sorted = sorted(((v["val"], k) for k, v in lf.items() if not k.startswith("ablation")),
                   reverse=True)
lf_rank = [k for _, k in lf_sorted].index(SUBMITTED) + 1
lf_gap = lf_sorted[0][0] - [v for v, k in lf_sorted if k == SUBMITTED][0]
assert lf_gap < 0.01, lf_sorted                              # LastFM is a near-tie at the top
exp_names = ["local+expander+virtual", "local+expander8+virtual"]
assert set(k for _, k in lf_sorted[-2:]) == set(exp_names), lf_sorted     # expanders last there
assert set(sorted(STRAT_KEYS, key=mean3)[-2:]) == set(exp_names)          # and on ZINC
ball, lv, exp = mean3(SUBMITTED), mean3("local+virtual"), mean3("local+expander+virtual")
wins = sum(q2[f"sparse: {SUBMITTED}"]["test"] < q2["sparse: local+virtual"]["test"] for _ in (0,)) \
    + sum(seeds[sd][f"sparse: {SUBMITTED}"]["test"] < seeds[sd]["sparse: local+virtual"]["test"]
          for sd in (1, 2))
q2prose = (
    "ZINC says the ranking is not the one the pair counts suggest. Restricting attention to the "
    "graph beats full attention outright --- %.4f against %.4f test MAE on the three-seed mean "
    "--- so on 23-atom molecules the sparsity is a useful prior, not a sacrifice. Two hops wins "
    "again, at %d of the 3 seeds and by %.4f on the mean, while a random expander of comparable "
    "size loses %.4f: the pairs have to mean something, and an expander edge means nothing to a "
    "molecule. LastFM neither contradicts nor confirms that --- its top three finish within "
    "%.3f validation micro-F1, the submitted set %s of five --- so ZINC decides. What LastFM "
    "shows instead is the cost: %.2f\\,s a step against %.2f\\,s for full attention over all %s "
    "pairs, a %.0f$\\times$ saving, at test micro-F1 %.4f."
) % (lv, fm, wins, lv - ball, exp - ball,
     lf_sorted[0][0] - lf_sorted[2][0],
     {1: "first", 2: "second", 3: "third"}.get(lf_rank, f"ranked {lf_rank}"),
     bench[f"sparse: {SUBMITTED}"][1], bench["full: LapPE + SPD"][1],
     f"{bench['full: LapPE + SPD'][0]:,}".replace(",", "{,}"),
     bench["full: LapPE + SPD"][1] / bench[f"sparse: {SUBMITTED}"][1],
     lf[SUBMITTED]["test"])

tex = (TEX.replace("%%HELPERS%%", HELPERS).replace("%%Q1CODE%%", Q1CODE)
       .replace("%%Q2CODE%%", Q2CODE)
       .replace("%%ZINC_Q1_TABLE%%", t1).replace("%%ZINC_Q2_TABLE%%", t2)
       .replace("%%LASTFM_TABLE%%", t3)
       .replace("%%Q1_RESULT_PROSE%%", q1prose)
       .replace("%%Q2_RESULT_PROSE%%", q2prose)
       .replace("%%BALL_ZINC%%", f"{counts[SUBMITTED]['pairs']:.0f}")
       .replace("%%BALL_LASTFM%%", f"{bench[f'sparse: {SUBMITTED}'][0]:,}".replace(",", "{,}")))

os.makedirs(OUT, exist_ok=True)
open(f"{OUT}/answer.tex", "w").write(tex.lstrip("\n"))
open(f"{OUT}/preamble.txt", "w").write(
    "\\usepackage{listings}\n\\usepackage{xcolor}\n\\usepackage{booktabs}\n"
    "\\usepackage{float}\n\\usepackage{amsmath}\n\\usepackage{amssymb}\n")
words = len(re.sub(r"\\begin\{lstlisting\}.*?\\end\{lstlisting\}", " ", tex, flags=re.S).split())
print(f"wrote {OUT}/answer.tex  ({len(tex.splitlines())} lines, ~{words} words incl. tables/macros)")
