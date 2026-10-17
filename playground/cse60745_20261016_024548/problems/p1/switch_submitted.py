"""Point SparseSPDAttention at the pair set that won on validation (the 2-hop ball plus one
global virtual node) and keep the Exphormer-style expander variants in experiments.py.

The five pair sets themselves do not change -- only which class holds which one -- so every
number already measured stays valid for its strategy name.  verify_switch.py checks that the
new SparseSPDAttention.attention_pairs is identical, pair for pair, to the Ball2SPDAttention
that produced those numbers, and run_cell18.py re-runs ZINC end to end to confirm it.

  python3 switch_submitted.py
"""
s = open("solution.py").read()
old = '''class SparseSPDAttention(SPDAttention):
    """Your Q1 attention, restricted to a chosen set of node pairs (Exphormer-style:
    graph neighbourhood + expander + one global virtual node)."""'''
new = '''class SparseSPDAttention(SPDAttention):
    """Your Q1 attention, restricted to a chosen set of node pairs.

    Of the five pair sets measured (see the report) the 2-hop ball plus one global virtual node
    had the lowest validation MAE on ZINC and the highest validation micro-F1 on LastFM, so that
    is what this class attends to.  pair_set below still builds Exphormer's random expander; the
    expander variants are one argument away and are compared in the report."""'''
assert old in s
s = s.replace(old, new)
old2 = '''    @staticmethod
    def attention_pairs(edge_index, num_nodes):
        return pair_set(edge_index, num_nodes, n_cycles=EXPANDER_CYCLES, virtual=True)'''
new2 = '''    @staticmethod
    def attention_pairs(edge_index, num_nodes):
        """Every ordered pair at most two hops apart, plus one global virtual node."""
        n = num_nodes
        A = sp.coo_matrix((np.ones(edge_index.size(1)), (edge_index[0].numpy(), edge_index[1].numpy())),
                          shape=(n, n)).tocsr()
        ball = ((A + A @ A) > 0).tocoo()                   # pairs at distance 0, 1 or 2
        extra = torch.from_numpy(np.stack([ball.row, ball.col])).long()
        return pair_set(edge_index, num_nodes, n_cycles=0, virtual=True, extra=[extra])'''
assert old2 in s
open("solution.py", "w").write(s.replace(old2, new2))

e = open("experiments.py").read()
old3 = '''class Ball2SPDAttention(SparseSPDAttention):
    """2-hop ball + one global virtual node (a dense local window instead of an expander)."""

    @staticmethod
    def attention_pairs(edge_index, num_nodes):
        n = num_nodes
        A = sp.coo_matrix((np.ones(edge_index.size(1)), (edge_index[0].numpy(), edge_index[1].numpy())),
                          shape=(n, n)).tocsr()
        ball = ((A + A @ A) > 0).tocoo()                    # pairs at distance 1 or 2
        extra = torch.from_numpy(np.stack([ball.row, ball.col])).long()
        return pair_set(edge_index, num_nodes, n_cycles=0, virtual=True, extra=[extra])'''
new3 = '''class Expander2SPDAttention(SparseSPDAttention):
    """1-hop neighbourhood + a 4-regular expander + one global virtual node (Exphormer)."""

    @staticmethod
    def attention_pairs(edge_index, num_nodes):
        return pair_set(edge_index, num_nodes, n_cycles=2, virtual=True)'''
assert old3 in e
e = e.replace(old3, new3)
old4 = '''    "local+expander+virtual": SparseSPDAttention,           # the submitted one
    "local+expander8+virtual": Expander4SPDAttention,
    "2-hop ball+virtual": Ball2SPDAttention,'''
new4 = '''    "local+expander+virtual": Expander2SPDAttention,
    "local+expander8+virtual": Expander4SPDAttention,
    "2-hop ball+virtual": SparseSPDAttention,               # the submitted one'''
assert old4 in e
open("experiments.py", "w").write(e.replace(old4, new4))
print("SparseSPDAttention now attends: the 2-hop ball + one global virtual node")
