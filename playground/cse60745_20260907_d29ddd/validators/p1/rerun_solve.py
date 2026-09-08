"""Part A: Q1 graph creation + Q2 modification, with both figures.

Run with /home/xing/miniconda3/envs/py311/bin/python (has networkx + matplotlib).
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx

OUT = '/home/xing/project/auto_hw_complete/playground/cse60745_20260907_d29ddd/validators/p1/rerun'
PREVIEW = ('/home/xing/project/auto_hw_complete/playground/cse60745_20260907_d29ddd/validators/p1/rerun'
           )
os.makedirs(OUT, exist_ok=True)
os.makedirs(PREVIEW, exist_ok=True)

# ---------------------------------------------------------------- Q1 -----
EDGES = [(0, 1), (0, 4), (0, 5),
         (1, 2), (1, 6),
         (2, 3), (2, 7),
         (3, 4), (3, 8),
         (4, 9),
         (5, 7), (5, 8),
         (6, 8), (6, 9),
         (7, 9)]

G = nx.Graph()
G.add_nodes_from(range(10))
G.add_edges_from(EDGES)

print('=== Q1 ===')
print('nodes:', G.number_of_nodes(), sorted(G.nodes()))
print('edges:', G.number_of_edges())
print('edge list:', sorted(tuple(sorted(e)) for e in G.edges()))
deg = dict(G.degree())
print('degrees:', [deg[v] for v in range(10)])
print('degree sum:', sum(deg.values()), '= 2*E =', 2 * G.number_of_edges())
print('3-regular:', all(d == 3 for d in deg.values()))
print('connected:', nx.is_connected(G), 'components:', nx.number_connected_components(G))
print('girth (shortest cycle):', min(len(c) for c in nx.cycle_basis(G)) if G.number_of_edges() else None)
print('triangles:', sum(nx.triangles(G).values()) // 3)
print('isomorphic to Petersen graph:',
      nx.is_isomorphic(G, nx.petersen_graph()))

# Layout: the measured pixel centres of the node discs in the assignment
# figure (y flipped, since image y grows downward).  Deterministic, and it
# reproduces the drawing in the assignment so the two can be compared
# directly.  The same positions are reused for Q2.
CENTRES = {0: (78.49, 43.30),  8: (290.40, 91.35),  4: (210.38, 121.02),
           6: (372.43, 196.78), 5: (74.83, 213.08), 1: (194.39, 260.64),
           3: (340.37, 322.77), 9: (244.40, 369.22), 7: (96.38, 483.11),
           2: (234.74, 530.73)}
POS = {v: (x, -y) for v, (x, y) in CENTRES.items()}


def draw(graph, path, highlight_isolated=True):
    fig, ax = plt.subplots(figsize=(4.6, 5.6))
    iso = [v for v in graph if graph.degree(v) == 0]
    normal = [v for v in graph if graph.degree(v) > 0]
    # Nodes 5, 4, 8 are almost exactly collinear, so a straight edge (5,8)
    # would pass through the disc of node 4 and read as "5-4 and 4-8".
    # Bow that one edge slightly so the drawing is unambiguous.
    bowed = [e for e in graph.edges() if set(e) == {5, 8}]
    straight = [e for e in graph.edges() if set(e) != {5, 8}]
    nx.draw_networkx_edges(graph, POS, edgelist=straight, ax=ax,
                           width=1.6, edge_color='#444444')
    assert len(bowed) == 1, f'expected edge (5,8) to be present, got {bowed}'
    # connectionstyle is only honoured on the FancyArrowPatch path, which
    # networkx takes when arrows=True; the undirected default (LineCollection)
    # silently ignores it.
    nx.draw_networkx_edges(graph, POS, edgelist=bowed, ax=ax,
                           width=1.6, edge_color='#444444',
                           arrows=True, arrowstyle='-',
                           connectionstyle='arc3,rad=0.30')
    nx.draw_networkx_nodes(graph, POS, nodelist=normal, ax=ax,
                           node_size=760, node_color='#3a7ab5',
                           edgecolors='#20415f', linewidths=1.2)
    if iso and highlight_isolated:
        nx.draw_networkx_nodes(graph, POS, nodelist=iso, ax=ax,
                               node_size=760, node_color='#d9863b',
                               edgecolors='#7a4715', linewidths=1.2)
    nx.draw_networkx_labels(graph, POS, ax=ax, font_size=13,
                            font_weight='bold', font_color='white')
    ax.set_axis_off()
    ax.margins(0.08)
    fig.tight_layout(pad=0.2)
    fig.savefig(path, format='pdf', bbox_inches='tight')
    # PNG preview goes to the PLAYGROUND, never to OUTPUT (rule R4)
    preview = os.path.join(PREVIEW, os.path.basename(path).replace('.pdf', '.png'))
    fig.savefig(preview, dpi=170, bbox_inches='tight')
    plt.close(fig)


draw(G, os.path.join(OUT, 'fig_p1_q1_graph.pdf'))

# ---------------------------------------------------------------- Q2 -----
H = G.copy()
H.remove_node(1)
H.remove_edge(0, 4)
H.remove_edge(0, 5)

print('\n=== Q2 ===')
print('removed node 1 (and its incident edges), then edges (0,4) and (0,5)')
print('nodes:', H.number_of_nodes(), sorted(H.nodes()))
print('edges:', H.number_of_edges())
print('edge list:', sorted(tuple(sorted(e)) for e in H.edges()))
comps = sorted((sorted(c) for c in nx.connected_components(H)), key=len)
print('number of connected components:', len(comps))
for k, c in enumerate(comps, 1):
    sub = H.subgraph(c)
    print(f'  component {k}: size={len(c)} nodes={c} edges={sub.number_of_edges()}')
print('degrees:', {v: H.degree(v) for v in sorted(H.nodes())})

draw(H, os.path.join(OUT, 'fig_p1_q2_graph.pdf'))
print('\nwrote figures to', OUT)
