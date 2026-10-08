"""fig_p1_depth.pdf -- test MRR against receptive-field depth, MyGCNConv vs MyDeepConv.
Mean over seeds 0/1/2 with a min-max band. Numbers from logs/sweep_seeds.json."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt

matplotlib.rcParams.update({
    "pdf.fonttype": 42,                 # embed TrueType, never Type 3
    "font.size": 10, "axes.labelsize": 11, "legend.fontsize": 9.5,
    "xtick.labelsize": 10, "ytick.labelsize": 10,
})

OUT = Path("/home/xing/project/auto_hw_complete/output/cse60745_20261006_e5b94a/p1")
sweep = json.load(open("logs/sweep_seeds.json"))

BLUE, ORANGE = "#2a78d6", "#eb6834"     # categorical slots 1 and 2, validator-passed
SERIES = [("MyGCNConv: 1 hop per layer", "MyGCNConv", BLUE, "o"),
          ("MyDeepConv: $K$ hops, 1 layer", "MyDeepConv", ORANGE, "s")]

fig, ax = plt.subplots(figsize=(5.4, 3.5))
ax.set_axisbelow(True)
ax.grid(axis="y", color="#dcdcd8", linewidth=0.6)

for label, key, colour, marker in SERIES:
    d = sweep[key]
    xs = sorted(int(k) for k in d)
    runs = [d[str(x)] for x in xs]
    mean = [sum(r) / len(r) for r in runs]
    ax.fill_between(xs, [min(r) for r in runs], [max(r) for r in runs],
                    color=colour, alpha=0.18, linewidth=0, zorder=2)
    ax.plot(xs, mean, "-", color=colour, marker=marker, markersize=7, linewidth=2,
            markeredgecolor="white", markeredgewidth=1.0, label=label, clip_on=False,
            zorder=3)
    # one direct label per series, at the 8-hop end: that is the claim being made
    ax.annotate(f"{mean[-1]:.3f}", (xs[-1], mean[-1]), textcoords="offset points",
                xytext=(-4, 10 if key == "MyDeepConv" else -17), ha="right",
                fontsize=10, color="#52514e")

ax.set_xlabel("Receptive field (hops)")
ax.set_ylabel("Test MRR")
ax.set_xticks([2, 4, 6, 8])
ax.set_xlim(1.8, 8.4)
ax.set_ylim(0.33, 0.80)
ax.set_yticks([0.4, 0.5, 0.6, 0.7, 0.8])
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_color("#9a9a95")
ax.tick_params(colors="#52514e", length=3)
# below the axes: the plot area has no gap wide enough for a legend box
ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.20), ncol=2,
          handlelength=2.2, columnspacing=1.6, borderpad=0)

fig.tight_layout(pad=0.4)
OUT.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT / "fig_p1_depth.pdf")
fig.savefig("logs/fig_p1_depth_preview.png", dpi=200)
print("wrote", OUT / "fig_p1_depth.pdf")
