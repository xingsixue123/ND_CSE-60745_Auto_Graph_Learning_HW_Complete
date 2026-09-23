#!/usr/bin/env python3
"""Gantt charts for Ex 2.1, straight out of schedules.json (no hand-typed blocks)."""
import json
import sys

import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

matplotlib.rcParams.update({
    "pdf.fonttype": 42,
    "font.family": "serif",
    "font.size": 9,
})

OUT = sys.argv[1].rstrip("/")
SCHED = json.load(open("schedules.json"))

ROWS = [1, 2, 3, 4]                      # T1 on top
COLOR = {1: "#6fa8dc", 2: "#f6b26b", 3: "#93c47d", 4: "#c9a0dc"}
ARR = {1: 1, 2: 2, 3: 3, 4: 4}
END = 22


def draw(policy, fname):
    blocks = SCHED[policy]["blocks"]
    fig, ax = plt.subplots(figsize=(6.0, 2.35))

    nrow = len(ROWS) + 1                 # + the idle row
    h = 0.50

    def ypos(tid):                       # row centre, T1 top
        return nrow - 1 - ROWS.index(tid)

    for who, s, e in blocks:
        if who is None:
            ax.broken_barh([(s, e - s)], (0 - h / 2, h),
                           facecolors="#e6e6e6", edgecolors="black",
                           linewidth=0.7, hatch="//")
        else:
            y = ypos(who)
            ax.broken_barh([(s, e - s)], (y - h / 2, h),
                           facecolors=COLOR[who], edgecolors="black", linewidth=0.7)
            if e - s >= 2:
                ax.text((s + e) / 2, y, f"T{who}", ha="center", va="center",
                        fontsize=8.5)

    # arrival instants
    for tid, a in ARR.items():
        y = ypos(tid)
        ax.plot([a], [y + h / 2 + 0.30], marker="v", markersize=5.0,
                color="black", clip_on=False, zorder=5)
        ax.vlines(a, y - h / 2, y + h / 2 + 0.30, color="black",
                  linewidth=0.7, linestyle=(0, (2, 2)), zorder=4)

    ax.set_yticks(list(range(nrow)))
    ax.set_yticklabels(["CPU idle"] + [f"T{t}" for t in reversed(ROWS)], fontsize=9)
    ax.set_ylim(-0.75, nrow - 1 + 0.75)

    ax.set_xticks(range(0, END + 1))
    ax.set_xlim(0, END)
    ax.set_xlabel("time (units)", fontsize=9)
    ax.tick_params(axis="x", labelsize=8, length=3)
    ax.set_axisbelow(True)
    ax.xaxis.grid(True, color="#bbbbbb", linewidth=0.4)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)

    ax.legend(handles=[plt.Line2D([], [], marker="v", linestyle="none",
                                  color="black", markersize=5, label="arrival"),
                       Patch(facecolor="#e6e6e6", edgecolor="black",
                             hatch="//", label="idle")],
              loc="upper right", bbox_to_anchor=(1.0, 1.20),
              ncol=2, frameon=False, fontsize=8, handletextpad=0.5,
              columnspacing=1.2)

    fig.tight_layout()
    fig.savefig(f"{OUT}/{fname}")
    plt.close(fig)
    print("wrote", f"{OUT}/{fname}")


draw("RR", "fig_p1_rr.pdf")
draw("FIFO", "fig_p1_fifo.pdf")
draw("SJF", "fig_p1_sjf.pdf")
