"""Make the random sign flip conditional on the batch holding more than one graph.

The flip is a data augmentation over graphs: it teaches the model that v and -v are the same
encoding. LastFM is one graph trained full-batch, so there is nothing to generalise over --
every step sees the same node set under a fresh random sign pattern, and evaluation sees yet
another. Measured on LastFM (2-hop ball pair set, 200 epochs): flipping costs ~0.12 micro-F1.
ZINC is unaffected: its batches hold 128 training / 256 evaluation graphs.
"""
s = open("solution.py").read()
old = '''    def inject_absolute(self, h, batch):
        lap = batch["lap"]
        if self.training:                                # eigenvectors are defined up to sign:
            sign = torch.randint(0, 2, (batch["num_graphs"], lap.size(1)),  # flip at random while
                                 device=lap.device, dtype=lap.dtype) * 2 - 1  # training, identity
            lap = lap * sign[batch["batch"]]                                  # at evaluation
        return h + self.lap_proj(lap)'''
new = '''    def inject_absolute(self, h, batch):
        lap = batch["lap"]
        # Eigenvectors are defined up to sign, so flip each graph's channels at random while
        # training and use the identity at evaluation.  This is an augmentation ACROSS graphs:
        # on a single-graph batch there is nothing to generalise over and the flip is pure
        # input noise, so it is skipped (it costs ~0.12 micro-F1 on LastFM).
        if self.training and batch["num_graphs"] > 1:
            sign = torch.randint(0, 2, (batch["num_graphs"], lap.size(1)),
                                 device=lap.device, dtype=lap.dtype) * 2 - 1
            lap = lap * sign[batch["batch"]]
        return h + self.lap_proj(lap)'''
assert old in s
open("solution.py", "w").write(s.replace(old, new))

e = open("experiments.py").read()
old2 = '''class NoFlipLapPETransformer(LapPETransformer):
    """Ablation: no random sign flip, i.e. the arbitrary sign ARPACK/LAPACK returns is kept."""

    def inject_absolute(self, h, batch):
        return h + self.lap_proj(batch["lap"])'''
new2 = '''class NoFlipLapPETransformer(LapPETransformer):
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
        return h + self.lap_proj(lap)'''
assert old2 in e
open("experiments.py", "w").write(e.replace(old2, new2))
print("sign flip is now conditional on a multi-graph batch")
