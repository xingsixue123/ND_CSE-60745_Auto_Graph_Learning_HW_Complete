"""Masking-strategy variants of SparseSPDAttention (Q2) and pair-counting helpers.

Only `SparseSPDAttention` from solution.py is the submitted answer; these subclasses
exist to measure the alternatives the question asks us to compare.
"""
import math

import numpy as np
import scipy.sparse as sp
import torch

from gt_framework import *                                  # noqa: F401,F403
from solution import (LapPETransformer, SparseSPDAttention, laplacian_eigvecs, pair_set)


class LocalSPDAttention(SparseSPDAttention):
    """Self loops + the graph's edges only: attention restricted to the 1-hop neighbourhood."""

    @staticmethod
    def attention_pairs(edge_index, num_nodes):
        return pair_set(edge_index, num_nodes, n_cycles=0, virtual=False)


class LocalVirtualSPDAttention(SparseSPDAttention):
    """1-hop neighbourhood + one global virtual node."""

    @staticmethod
    def attention_pairs(edge_index, num_nodes):
        return pair_set(edge_index, num_nodes, n_cycles=0, virtual=True)


class Expander2SPDAttention(SparseSPDAttention):
    """1-hop neighbourhood + a 4-regular expander + one global virtual node (Exphormer)."""

    @staticmethod
    def attention_pairs(edge_index, num_nodes):
        return pair_set(edge_index, num_nodes, n_cycles=2, virtual=True)


class Expander4SPDAttention(SparseSPDAttention):
    """1-hop neighbourhood + a wider (8-regular) expander + one global virtual node."""

    @staticmethod
    def attention_pairs(edge_index, num_nodes):
        return pair_set(edge_index, num_nodes, n_cycles=4, virtual=True)


STRATEGIES = {
    "local": LocalSPDAttention,
    "local+virtual": LocalVirtualSPDAttention,
    "local+expander+virtual": Expander2SPDAttention,
    "local+expander8+virtual": Expander4SPDAttention,
    "2-hop ball+virtual": SparseSPDAttention,               # the submitted one
}


def count_pairs(cls, graphs):
    """(mean pairs per graph, mean n^2 per graph, mean pairs per node) of a strategy."""
    p = np.array([cls.attention_pairs(g["edge_index"], g["n"]).size(1) for g in graphs], dtype=float)
    n = np.array([g["n"] for g in graphs], dtype=float)
    return p.mean(), (n ** 2).mean(), (p / n).mean()


# ---- ablations for the two Q1 design choices (not part of the submitted class) ----
class RawLapPETransformer(LapPETransformer):
    """Ablation: the same eigenvectors WITHOUT the sqrt(n) scaling (entries ~ 1/sqrt(n))."""

    @staticmethod
    def precompute(edge_index, num_nodes):
        return {"lap": laplacian_eigvecs(edge_index, num_nodes) / math.sqrt(num_nodes)}


class NoFlipLapPETransformer(LapPETransformer):
    """Ablation: no random sign flip, i.e. the arbitrary sign ARPACK/LAPACK returns is kept."""

    def inject_absolute(self, h, batch):
        return h + self.lap_proj(batch["lap"])


class AlwaysFlipLapPETransformer(LapPETransformer):
    """Ablation: flip while training even on a single-graph batch (the unconditional rule)."""

    def inject_absolute(self, h, batch):
        lap = batch["lap"]
        if self.training:
            sign = torch.randint(0, 2, (batch["num_graphs"], lap.size(1)),
                                 device=lap.device, dtype=lap.dtype) * 2 - 1
            lap = lap * sign[batch["batch"]]
        return h + self.lap_proj(lap)
