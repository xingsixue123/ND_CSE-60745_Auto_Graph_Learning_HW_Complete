"""p2 — produce the two required figures as vector PDFs."""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

from analyze import build_graph

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "/home/xing/project/auto_hw_complete/output/cse60745_20260907_d29ddd/p2"

plt.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "pdf.fonttype": 42,
    "savefig.bbox": "tight",
})

def draw_cc2(CC2, path, labels):
    """Draw the 2nd-largest CC. `labels` toggles node-id text."""
    # kamada_kawai is deterministic (circular init + BFGS), so the drawing is
    # reproducible without an RNG seed.
    pos = nx.kamada_kawai_layout(CC2)

    fig, ax = plt.subplots(figsize=(6.0, 5.2))
    nx.draw_networkx_edges(CC2, pos, ax=ax, edge_color="#9aa5b1",
                           width=0.9, alpha=0.9)
    degs = dict(CC2.degree())
    nodes = list(CC2.nodes())
    sc = nx.draw_networkx_nodes(
        CC2, pos, ax=ax, nodelist=nodes,
        node_size=[28 + 14 * degs[n] for n in nodes],
        node_color=[degs[n] for n in nodes],
        cmap=plt.get_cmap("viridis"),
        linewidths=0.4, edgecolors="white",
    )
    if labels:
        nx.draw_networkx_labels(CC2, pos, ax=ax, font_size=4.5)
    cb = fig.colorbar(sc, ax=ax, fraction=0.040, pad=0.02)
    cb.set_label("Node degree", fontsize=10)
    cb.ax.tick_params(labelsize=9)
    ax.set_axis_off()
    ax.margins(0.06)
    fig.savefig(path)
    plt.close(fig)


def fig_cc2(G):
    comps = sorted(nx.connected_components(G), key=len, reverse=True)
    CC2 = G.subgraph(comps[1]).copy()
    print(f"CC2: {CC2.number_of_nodes()} nodes, {CC2.number_of_edges()} edges")
    # deliverable: unlabelled (see notes.md for the readability comparison)
    draw_cc2(CC2, os.path.join(OUT, "fig_p2_cc2.pdf"), labels=False)
    # playground-only variant, used to justify the no-labels decision
    draw_cc2(CC2, os.path.join(HERE, "cc2_labelled_variant.pdf"), labels=True)


def fig_degree(G):
    from collections import Counter
    degs = [d for _, d in G.degree()]
    hist = Counter(degs)
    ks = sorted(hist)
    ns = [hist[k] for k in ks]
    n = G.number_of_nodes()
    ps = [c / n for c in ns]

    fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.0))

    ax = axes[0]
    ax.bar(ks, ns, color="#3b6ea5", edgecolor="none", width=0.85)
    ax.set_xlabel("Degree $k$")
    ax.set_ylabel("Number of nodes $N(k)$")
    ax.set_title("Linear scale", fontsize=11)
    ax.set_xlim(-0.8, max(ks) + 1)
    ax.grid(axis="y", alpha=0.3, lw=0.5)

    ax = axes[1]
    ax.loglog(ks, ps, "o", ms=5, color="#b5432f",
              mec="white", mew=0.5)
    ax.set_xlabel("Degree $k$")
    ax.set_ylabel("Fraction of nodes $P(k)$")
    ax.set_title("Log-log scale", fontsize=11)
    ax.grid(which="both", alpha=0.25, lw=0.5)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_p2_degree_dist.pdf"))
    plt.close(fig)


def main():
    os.makedirs(OUT, exist_ok=True)
    G, _ = build_graph()
    fig_cc2(G)
    fig_degree(G)
    print("wrote figures to", OUT)


if __name__ == "__main__":
    main()
