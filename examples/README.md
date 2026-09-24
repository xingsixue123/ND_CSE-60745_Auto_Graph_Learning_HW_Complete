# Worked example — CSE 60745 HW2 Part (B), graph embedding

The first assignment that asks for an experiment rather than an answer. The work is
to implement random-walk sampling and SkipGram embeddings over the LastFM Asia social
network, then use the embeddings for friend recommendation and country classification,
and say what different sampling strategies contribute. It is also the first run whose
specification lives in a Jupyter notebook rather than a PDF.

## Where these files originally lived

| file, as it is here | where it was during the run |
|---|---|
| `specs.md` | `auto_hw_complete/specs.md` |
| `input/CSE60745-Hands-on_HW2-Part(B)-1.pdf` | `auto_hw_complete/input/…` |
| `input/graph_embedding-1.ipynb` | `auto_hw_complete/input/…` |
| `output/cse60745_20260923_8654c1/` | `auto_hw_complete/output/…` |
| `playground/cse60745_20260923_8654c1/` | `auto_hw_complete/playground/…` |

Excluded from the repository: the 547 MB virtual environment the master built, the
dataset the notebook's own setup cell downloads, and the pickled result objects. All
three are reproducible; `downloads.md` records every install and every URL.

## Three things this run needed that earlier ones did not

**A notebook is not a data file.** `.ipynb` was landing in the `data` bucket, so the
file the specification called "where the real hw guideline and problem definitions
are" would have reached the master as 600 characters of JSON metadata. `ingest.py`
now flattens a notebook to its cells in order, markdown as prose and code as code,
and drops cell outputs deliberately: they are the previous author's results, and an
agent that reads them may report them instead of running the code itself.

**The master needed its own timeout.** It is a coordinator, not a worker: it sits
blocked inside `fw spawn-worker` for the whole of every problem, so its wall clock is
the sum of every agent's. Here p1's worker ran 42 minutes and p2's ran 50, and the
master was killed by the 2-hour worker limit with p2 unvalidated and nothing
assembled. `master_timeout_seconds` now covers it separately. Nothing was lost:
`fw resume` cleared p2's stale `running` flag, handed the master back its own session
with a summary of what was finished, and it carried on from there.

**The master built a shared environment.** Rather than letting each worker install
its own, it created one venv with gensim, scipy, scikit-learn, pandas, networkx and
matplotlib, fetched the dataset exactly as the notebook's setup cell does, and pointed
both workers at it.

## The defect worth reading

`playground/.../validators/p1/checklist.md`, round 1. The validator re-ran the
experiment rather than reading the worker's numbers, and its first defect is not a
compliance point:

> Country validation macro-F1 is never reported … The number already exists:
> `evaluate_country` returns it, and `make_tables.py:31` computes it as `cc_val_macro`
> and then drops it from `ORDER` at lines 37–38. This is not just compliance — I
> computed the column and it is the worker's **strongest remaining evidence**: spread
> 0.0411 against a noise floor of 0.0077, ratio 5.35×, second only to val H@1 …
> Omitting it throws away the result that best supports the answer's own thesis.

It also caught a metric mismatch (a Hit@1 gap divided by an MRR spread, giving 50×
where the right answer is 32×), a sentence whose own numbers refuted it ("as cheap as
DeepWalk … 1.9 s versus 0.7 s"), and the observation that the analysis led with
validation columns that are themselves the model-selection criteria.

## How the run went

| | |
|---|---|
| wall clock | about 3 hours 10 minutes, including the 2 hours lost to the timeout |
| cost | $92.72 |
| p1 (Task 3, 30 pts) | failed round 1, passed round 2 |
| p2 (Task 4, optional) | passed on round 3 |
| master validation | FAIL, FAIL, then PASS |

The most expensive run so far by a wide margin, and the reason is that this one
actually trains models: p1's worker alone cost $16.81 and produced seven sampling
strategies across thirteen metrics with a multi-seed repeat and a random control.

No length rule was in force for this run; `specs.md` had been rewritten without R8
and R9. p1 came out at 87 words per point, against 53 for the whole of the assignment
that did carry them.

## Reproducing it

```bash
cp examples/specs.md .
cp examples/input/* input/
framework/fw run
```
