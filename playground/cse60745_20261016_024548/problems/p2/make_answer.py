"""Build OUTPUT/answer.tex. The code listing is read out of hybrid_layer.py and every
number in the table is read out of logs/, so nothing in the deliverable is hand-copied."""
import re, glob, statistics as st, pathlib, sys

OUT = pathlib.Path(__import__("os").environ.get(
    "OUTDIR", "/home/xing/project/auto_hw_complete/output/cse60745_20261016_024548/p2"))

# ---------- 1. the code, verbatim out of the file that was run ----------
src = pathlib.Path("hybrid_layer.py").read_text()
listing = src.split("class HybridGTLayer(nn.Module):")[1].split("\nclass HybridGT(")[0]
listing = "class HybridGTLayer(nn.Module):" + listing.rstrip() + "\n"
assert max(len(l) for l in listing.splitlines()) <= 82, "listing line too wide"

# ---------- 2. the numbers, out of the logs ----------
runs = {}
LOGDIR = __import__("os").environ.get("LOGDIR", "logs")
for f in sorted(glob.glob(f"{LOGDIR}/*.log")):
    for line in open(f):
        m = re.match(r"### result (\S+) seed=(\d+) epochs=(\d+) val=([\d.]+) test=([\d.]+) "
                     r"epoch=(\d+) params=(\d+)", line)
        if m:
            name, seed, ep, val, test, be, pr = m.groups()
            runs.setdefault((name, int(ep)), []).append(
                dict(seed=int(seed), val=float(val), test=float(test),
                     best_epoch=int(be), params=int(pr)))


def agg(name, epochs=30):
    rs = sorted(runs[(name, epochs)], key=lambda r: r["seed"])
    v, t = [r["val"] for r in rs], [r["test"] for r in rs]
    sd = lambda a: st.stdev(a) if len(a) > 1 else 0.0
    return dict(n=len(rs), val=st.mean(v), val_sd=sd(v), test=st.mean(t), test_sd=sd(t),
                params=rs[0]["params"], epochs=[r["best_epoch"] for r in rs])


ROWS = [
    ("baseline-plain",  r"plain graph transformer (no structural information)"),
    ("baseline-demo",   r"demo: degree centrality + common-neighbour bias"),
    None,
    ("hybrid",          r"\textbf{hybrid GT (cell 22): parallel sum}"),
    ("local-only",      r"\quad ablation: global branch removed"),
    ("global-only",     r"\quad ablation: local branch removed"),
    None,
    ("sequential",      r"\quad instead: attention reads the MPNN output"),
    ("gated",           r"\quad instead: a learned gate in place of the sum"),
]

lines = []
for row in ROWS:
    if row is None:
        lines.append(r"    \midrule")
        continue
    key, label = row
    a = agg(key)
    cells = [label,
             "%.3f" % a["val"], "%.3f" % a["val_sd"],
             "%.3f" % a["test"], "%.3f" % a["test_sd"],
             "%.1fk" % (a["params"] / 1000), str(a["n"])]
    lines.append("    " + " & ".join(cells) + r" \\")
table = "\n".join(lines)

long = {k[0]: agg(k[0], 100) for k in runs if k[1] == 100}

HEAD = pathlib.Path("answer_head.tex").read_text().rstrip()

FIG = r"""
\begin{figure}[H]
  \centering
  \includegraphics[width=0.78\linewidth]{fig_p2_layer.pdf}
  \caption{One \texttt{HybridGTLayer}. Both branches read $x^{(\ell)}$; dashed arrows are
           residual connections.}
  \label{p2:fig:layer}
\end{figure}
"""

LST = r"""
\subsection*{Implementation}

\lstdefinestyle{p2python}{%
  language=Python, basicstyle=\footnotesize\ttfamily,
  keywordstyle=\color{blue!55!black}, commentstyle=\itshape\color{black!55},
  stringstyle=\color{green!35!black}, showstringspaces=false,
  breaklines=true, breakatwhitespace=true, keepspaces=true,
  frame=single, rulecolor=\color{black!30}, framerule=0.3pt,
  xleftmargin=4pt, xrightmargin=2pt, aboveskip=8pt, belowskip=4pt,
}

\noindent\texttt{HybridGT} (cell~22) is used unchanged.

\begin{lstlisting}[style=p2python]
""" + listing + r"""\end{lstlisting}
"""

TABLE = r"""
\subsection*{Results}

\begin{table}[H]
  \centering
  \small
  \caption{ZINC, 30 epochs; lower MAE is better, and the epoch is selected on validation
           MAE. Each row is the mean over independent runs at different seeds, with their
           standard deviation. Repeating a single configuration unchanged already moves test
           MAE by a comparable amount on this CPU, so the sd is a run-to-run noise floor
           rather than a seed effect alone. ``params'' counts only parameters that receive a
           gradient, so an ablation is not credited with the branch it never calls. The
           bold row is the submitted layer, not the best number in the column.}
  \label{p2:tab:zinc}
  \begin{tabular}{lrrrrrr}
    \toprule
    & \multicolumn{2}{c}{val MAE} & \multicolumn{2}{c}{test MAE} & & \\
    \cmidrule(lr){2-3}\cmidrule(lr){4-5}
    model & mean & sd & mean & sd & params & runs \\
    \midrule
""" + table + r"""
    \bottomrule
  \end{tabular}
\end{table}
"""

# --- the run-to-run noise floor, measured by repeating ONE configuration unchanged ---
# logs_det/: three runs of `local-only seed 0 epochs 30`, two at 4 torch threads and one at
# 1, all at the same seed. They do not agree, so this spread -- not the seed spread alone --
# is the bar a difference has to clear.
_det = []
for _f in sorted(glob.glob("logs_det/*.log")):
    for _line in open(_f):
        _m = re.search(r"### result \S+ seed=\d+ epochs=\d+ val=[\d.]+ test=([\d.]+)", _line)
        if _m:
            _det.append(float(_m.group(1)))
assert len(_det) >= 2, "logs_det/ must hold at least two repeats of one configuration"
_noise = max(_det) - min(_det)

# --- guard every comparative claim the prose makes ---
_h, _l, _g = agg("hybrid"), agg("local-only"), agg("global-only")
_s, _ga = agg("sequential"), agg("gated")
assert abs(_h["test"] - _l["test"]) <= _noise, (
    f"prose: removing attention changes nothing beyond noise, but "
    f"|{_h['test']:.4f}-{_l['test']:.4f}| > {_noise:.4f}")
assert abs(_s["test"] - _h["test"]) <= _noise, (
    f"prose: stacking matches summing, but the gap "
    f"{abs(_s['test'] - _h['test']):.4f} > {_noise:.4f}")
assert 0 < _h["test"] - _ga["test"] < 2 * _noise, (
    f"prose: the gate is ahead by about one noise width; the gap is "
    f"{_h['test'] - _ga['test']:.4f} against {_noise:.4f}")
assert _g["test"] - _h["test"] > 2 * _noise, "prose: removing message passing costs accuracy"
assert agg("baseline-plain")["test"] > _h["test"] and agg("baseline-demo")["test"] > _h["test"], (
    "prose: the hybrid beats both baselines")
assert all(e >= 28 for e in _h["epochs"]), (
    f"prose: every hybrid run peaks in the final three epochs; got {_h['epochs']}")
_have_long = {"hybrid", "local-only", "global-only"} <= set(long)
if _have_long:
    assert long["hybrid"]["test"] - long["local-only"]["test"] > _noise, (
        "prose: at 100 epochs local-only is ahead of the hybrid by more than noise")
    _longnote = (", and at 100 (one run each) the gap opens the other way --- local only"
                 " %.3f against %.3f" % (long["local-only"]["test"], long["hybrid"]["test"]))
else:
    _longnote = ""
    print("WARNING: no 100-epoch runs; that clause is omitted")
print(f"prose claims check out against the data (noise floor {_noise:.4f} "
      f"from {len(_det)} repeats)")

PROSE_TEMPLATE = r"""
The hybrid cuts the plain transformer's test MAE from %(plain).3f to %(hyb).3f and beats the
demo encoding at %(demo).3f. The ablation says which branch does it: removing attention
changes nothing beyond run-to-run noise (%(loc).3f), removing message passing costs
%(glo).3f. Repeating one configuration unchanged already moves test MAE by %(noise).3f here,
the bar the rest has to clear. Every hybrid run peaks in the final three epochs, so 30 stops
it early%(longnote)s. Stacking the branches matches summing them (%(seq).3f), and the gate is
the best of the three at %(gat).3f --- by about one noise width, and with %(gatep)d\%% more
parameters, so I kept the plain sum.

The global branch is not short of range: ZINC molecules have mean diameter $12.5$, and four
message-passing rounds cover only $51.8\%%$ of node pairs. It is short of \emph{identity}.
Degree centrality --- the absolute encoding \texttt{HybridGT} fixes --- takes four values and
gives half of all atoms the same one, so attention can average over a molecule but hardly
tell which atom it reads. Of GraphGPS's three ingredients, the one missing here is the first,
the positional/structural encoding.
"""

PROSE = PROSE_TEMPLATE % dict(
    plain=agg("baseline-plain")["test"], demo=agg("baseline-demo")["test"],
    hyb=_h["test"], loc=_l["test"], glo=_g["test"],
    seq=_s["test"], gat=_ga["test"], noise=_noise, longnote=_longnote,
    gatep=round(100 * (_ga["params"] / _h["params"] - 1)))
assert "%(" not in PROSE, "an unsubstituted placeholder is left in the prose"


OUT.mkdir(parents=True, exist_ok=True)
(OUT / "answer.tex").write_text(HEAD + "\n" + FIG + LST + TABLE + PROSE + "\n")
print("wrote", OUT / "answer.tex")

