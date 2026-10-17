"""Shared run wrapper: runs one ZINC task, records the result and the wall clock."""
import json
import time

from gt_framework import run_graph_task, EPOCHS_ZINC


def make_runner(path):
    results = {}

    def run(label, model):
        t0 = time.time()
        best = run_graph_task(label, model)
        best["s_per_epoch"] = (time.time() - t0) / EPOCHS_ZINC
        results[label] = best
        with open(path, "w") as f:
            json.dump(results, f, indent=1)
        return best

    return run, results
