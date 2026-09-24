# p2 — Task 4: Heterogeneous Graph Embedding (HW2-Part(B), Practice II, marked *Optional*)

Your problem id is **p2**. Every LaTeX label, figure filename and macro you define must
be namespaced with `p2:` / `fig_p2_` (rule R5).

---

## 0. Where this question lives

- Slide deck `input/CSE60745-Hands-on_HW2-Part(B)-1.pdf`, **rendered pages 10 and 11**.
  Page 10 is the divider: `Practice II: Heterogeneous Graph Embedding (Optional)`.
  Page 11 is the task slide, `Hands-on Practice: Heterogeneous Graph Embedding`.
  Ingested: `.../ingest/pages/CSE60745-Hands-on_HW2-Part(B)-1/page_011.png`, and the
  embedded figure at native resolution as `page_011_fig_02.jpeg`.
  **I have already read that figure.** It shows six user nodes U1..U6 (blue) connected
  to each other, and four artist nodes A1..A4 (orange) connected to users, with a
  purple arrow labelled **"U–A–U Meta-path"** running U1 → A1 → U2. It is an
  illustration of what a meta-path is; it carries no data or parameters. You do not
  need to redraw it.

- Jupyter notebook **`/home/xing/project/auto_hw_complete/input/graph_embedding-1.ipynb`**
  — the authoritative problem definition. Read it in full first. Your scope is
  **Task 4 (sections 7 and 8)**. Task 3 (sections 1–6) is problem p1 and is already
  done — you reuse its code, you do not redo it.

This practice is explicitly labelled **(Optional)** on rendered page 10. Treat it as a
genuine extension: do it properly, but if you have to trade breadth for correctness,
keep it correct and narrow and say what you left out.

---

## 1. Question text, transcribed from the notebook

> # Task 4 — Heterogeneous Graph Embedding
>
> **Dataset.** The same 7,624 users, plus a second kind of node: the **artists** they
> like, taken from the LastFM Asia "features" file and used as graph structure rather
> than as a feature vector.
>
> | Descriptor | Statistics |
> |---|---|
> | artists | 7,842 |
> | user–artist edges | 3,014,361 |
> | artists per user | median 400, max 944 |
>
> The heterogeneous graph `H_train` is `G_train` with the artist nodes and user–artist
> edges added. Artists get ids `N_USERS … N_USERS + N_ARTISTS − 1`, so users and artists
> share one integer id space and one embedding matrix; the `type` attribute is `"U"` or
> `"A"`.
>
> **Your job.** Implement a heterogeneous graph embedding method to learn new user
> embeddings enriched by heterogeneous graph structures. You can re-implement
> metapath2vec, following meta-path based graph embedding, or implement your own ideas.
> You can compare your Task 4 results with your Task 3 results in the same
> `comparison_table()`.
>
> **Where the code goes.** This task reuses everything from Task 3:
>
> | what | where |
> |---|---|
> | the sampler | `sample_walks` in section 3, extended so that a meta-path can be selected through the constructor; re-run that cell, then run section 8 below |
> | typed neighbour lists | `typed_adjacency(G)` from section 2: `ADJ_T[u]["A"]` are the artists user `u` likes, `ADJ_T[a]["U"]` the users who like artist `a` |
> | embedding training and both downstream models | unchanged from sections 3 and 4 |
> | evaluation | `run_experiment` from section 5, called with `H_train` instead of `G_train` and `N_USERS + N_ARTISTS` instead of `N_USERS` |
>
> Please run data loading cell below before you run experiments for Task 4.

And from the slide, rendered page 11:

> Given new "artist" nodes in LastFM-Asia, enrich user embeddings with heterogeneous
> graph structures for the same downstream tasks in Practice I. Implement existing
> graph embedding techniques or design your own embedding methods. Please follow the
> instructions for Task 4 in the same notebook. It is recommended to first re-implement
> metapath2vec, test different meta-path combinations, and then test your own ideas for
> random walk sampling strategy and other components.

The provided Task 4 data-loading cell (notebook section 7) is:

```python
hstats = json.loads(Path("data/task3/hetero_stats.json").read_text())
N_ARTISTS = hstats["n_artists"]
user_artist = pd.read_csv("data/task3/user_artist.csv.gz")

def add_artists(G_social):
    H = G_social.copy()
    H.add_nodes_from(range(N_USERS, N_USERS + N_ARTISTS), type="A")
    H.add_edges_from(user_artist.itertuples(index=False, name=None))
    return H

H_train = add_artists(G_train)
```

Note `run_experiment` slices the embedding to `[:N_USERS]` before evaluating, and the
degree buckets are always taken from `G_train` (the social graph), artists or not.

---

## 2. What you must actually do

1. **Reuse p1's code verbatim.** p1's finished, validator-passed implementation lives in
   `/home/xing/project/auto_hw_complete/playground/cse60745_20260923_8654c1/problems/p1/`
   (read-only to you — read it, copy it into your own playground, do not write there).
   Its `answer.tex` is at
   `/home/xing/project/auto_hw_complete/output/cse60745_20260923_8654c1/p1/answer.tex`.
   You **must** use p1's `train_embedding`, `LinkPredictor` and `CountryClassifier`
   **unchanged**, and the same Skip-Gram hyper-parameters, so that your Task 4 rows are
   directly comparable with p1's Task 3 rows in one table. The only thing that changes
   is the sampler and the graph. If you find a genuine bug in p1's code, do not silently
   "improve" it — fix it, and state in your write-up exactly what you changed and why,
   because it invalidates the comparison otherwise.
2. **Extend `sample_walks` with a meta-path-bounded sampler** (metapath2vec): the walk
   follows a repeating type schema, and at each step the next node is drawn uniformly
   from the neighbours of the required type. Select the schema through the constructor,
   as the notebook says.
3. **Run at least two meta-path schemas**, e.g. `U-A-U` and `U-U-A-U` (or `U-A-U-U`,
   `U-A-U-A-U`, ...). Compare them against each other and against p1's best homogeneous
   strategy.
4. Report the same metrics as p1 — link prediction Hit@1/MRR on val and test, and
   country classification micro-F1/macro-F1 — in **one combined table that also contains
   p1's Task 3 rows**, so the reader can see whether the artist structure helped.
5. **Analyse**: did the heterogeneous structure help friend recommendation, country
   classification, both, or neither? Artists are extremely dense (median 400 artists per
   user, 3.0M user–artist edges vs 19,464 social edges), so a U-A-U step connects users
   who share *any* artist — think about whether that is signal or noise, and whether it
   helps precisely the low-degree / cold-start users who have no social neighbours. The
   per-source-degree breakdown is the right tool for that claim; use it.

---

## 3. Data — already downloaded, do not re-download

```
/home/xing/project/auto_hw_complete/playground/cse60745_20260923_8654c1/data/
    task1/split_stats.json  task1/lp_graph_obs.csv
    task1/lp_train.csv      task1/lp_val.csv    task1/lp_test.csv
    task2/node_country.csv
    task3/hetero_stats.json task3/user_artist.csv.gz  task3/country_split.csv
```

Read-only to you: symlink or copy it into your playground as `data/`, do not write
there. Verified ground truth from `hetero_stats.json`: `n_users 7624`, `n_artists 7842`,
`artist_id_offset 7624`, `n_user_artist_edges 3014361`, `users_with_no_artist 173`.
Sanity-check your `H_train` against those numbers before you trust any result.

## 4. Environment — already set up, do not reinstall

```
/home/xing/project/auto_hw_complete/playground/cse60745_20260923_8654c1/venv/bin/python
```
gensim 4.4.0, numpy 2.4.6, scipy 1.17.1, scikit-learn 1.9.1, pandas, networkx 3.6.1,
matplotlib. 32 cores, ~114 GB RAM. Set `MPLCONFIGDIR` inside your playground before
importing matplotlib. Anything you install goes in your own playground and gets a line
in `downloads.md` (rule R3).

**Performance warning, read this before you start.** `H_train` has ~3.03M edges and
15,466 nodes. `nx.Graph.add_edges_from` on 3M rows and `typed_adjacency(H)` are each
slow-ish but fine once (tens of seconds, a few GB); what will kill you is rebuilding
them per walk or per strategy. Build `H_train` and its typed adjacency **once**, cache
them, and reuse across schemas. Artist neighbour lists average ~384 users, so sampling
a next node is O(1) with `random.choice` on a list — keep them as lists, not sets.
`embed_graph` starts a walk from **every** node of H (15,466 nodes, users and artists),
so a U-A-U schema starting from an artist has to be handled: either start with the
artist's type-appropriate schema rotation or return `[]` for artists and say so. Whatever
you choose, state it. Budget a few minutes per schema.

---

## 5. Deliverable

`answer.tex` in your OUTPUT dir, a **LaTeX fragment** (no `\documentclass`,
`\begin{document}` or `\usepackage`; extra packages go one per line in `preamble.txt`),
starting at `\section{...}`. It is a homework submission, not a lab notebook.

Contents:

1. Short statement of the method: the meta-path schemas tried, how the schema constrains
   the walk, what is reused unchanged from Task 3 (say this explicitly — it is what makes
   the comparison valid), and how artist-start nodes are handled.
2. A **compact code listing of the meta-path sampler only**. Do not re-paste p1's
   `train_embedding` / `LinkPredictor` / `CountryClassifier` — refer to them as
   "unchanged from Task 3". Do not paste scaffolding or debug output.
3. The **combined comparison table**: your Task 4 schemas *and* p1's Task 3 rows,
   as a real `booktabs` table. Take p1's numbers from p1's actual results (its playground
   / its `answer.tex`), do not re-run or re-estimate them.
4. The per-source-degree breakdown where it supports your argument, and at most one or
   two figures. Any figure must be a vector PDF named `fig_p2_<something>.pdf` in your
   OUTPUT dir, referenced by bare filename.
5. The analysis from §2.5 above.

Every number must come from a run you actually performed (or, for the Task 3 rows, from
p1's actual run). Do not fabricate. If a schema was too slow and you dropped it, say so.
Keep it tight — this is the optional practice; 2–4 pages is right.

---

# RESUME NOTE FROM THE MASTER — READ THIS FIRST (added 2026-09-23 17:5x)

**Your previous session already solved this problem. Do not start over.**

The run was interrupted by a *master-level* timeout, not by any failure of yours. The
framework's log records `p2 worker round 1 rc=0` — your worker round completed
successfully. What never happened is the validator audit, so the loop is being restarted
only to get you audited.

Already on disk and believed good (I, the master, have read them):

- `PLAYGROUND/submission.md` — written, complete
- `PLAYGROUND/run_hetero.log` + `results_hetero.{csv,pkl}` — 5 configurations
  (hetero-deepwalk, U-A-U, U-U-A-U, U-U-U-A-U, U-A-U rare-artist a=1) x seeds {0,1,2},
  all 15 runs finished
- `PLAYGROUND/results_control.pkl` + `control_budget.log` — the walk-budget control
- `OUTPUT/answer.tex`, `OUTPUT/fig_p2_degree.pdf`, `OUTPUT/fig_p2_social.pdf`,
  `OUTPUT/preamble.txt`

**What to do this round:** verify rather than recompute. Re-read your `submission.md`
and `answer.tex`, confirm the deliverable is intact and self-consistent (figures present,
labels namespaced `p2:`/`fig_p2_`, numbers in the tables match `results_hetero.pkl`,
`lint_output.py` clean, fragment still compiles), fix anything actually broken, and stop.

**Do NOT re-run `run_hetero.py`.** It costs ~50 minutes of GPU-less Skip-Gram training and
the results are already saved and seed-fixed; re-running would only burn the round budget.
The one exception: if you find a *genuine* bug that makes a reported number wrong. In that
case fix it, re-run only the affected configuration, and say so explicitly.

If everything checks out, simply confirm that in `submission.md` and finish the round.
