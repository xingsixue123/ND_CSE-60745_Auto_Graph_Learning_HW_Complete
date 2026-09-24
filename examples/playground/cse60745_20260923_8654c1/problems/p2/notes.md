# p2 — Task 4, Heterogeneous Graph Embedding. Plan.

## Source check (rule R7) — done before any code

Three channels on rendered pages 10 and 11 of `CSE60745-Hands-on_HW2-Part(B)-1.pdf`:

- `page_011.txt` — the slide bullets. Confirms "Metapath2vec: Meta-path bounded random
  walk sampling + Skip-gram contextualized embedding" and "recommended to first
  re-implement metapath2vec, test different meta-path combinations, and then test your
  own ideas for random walk sampling strategy".
- `page_011.png` — whole page, consistent with the text.
- `page_011_fig_01.png` (1536x1152) — **the Notre Dame slide template**, no content.
  `page_011_fig_02.jpeg` (507x338) — the cartoon: six blue user nodes U1..U6 joined to
  each other, four orange artist nodes A1..A4 joined to users, one purple arrow labelled
  "U-A-U Meta-path" running U1 -> A1 -> U2.

**Verdict: the figure is illustrative and carries no data or parameters.** Nothing to
transcribe, nothing to redraw. The master's brief said exactly this and it is correct.
The notebook `input/graph_embedding-1.ipynb` cells 14/15/16/17/18 are the authoritative
statement; I diffed the brief's transcription against the real cell text and found **no
discrepancy** — the brief quotes cell 14 and cell 16 word for word.

## What this problem needs

**code + diagram + plain.**

- *code*, mandatory. The deliverable is a table of measured metrics. Nothing estimated.
- *diagram*: the whole question is "did artist structure help, and for whom". The
  per-source-degree breakdown is the tool the brief names. One or two vector PDFs.
- *plain*: the analysis is the point of an optional extension task.

## Design decisions, fixed before running anything

1. **p1's code is reused byte-identically.** I copy `scaffold.py` and `impl.py` out of
   p1's playground and verify with sha256 that they are unmodified. My meta-path sampler
   is a *subclass* `MetaPathWalkEmbedding(WalkEmbedding)` that overrides `sample_walks`
   and nothing else, so `train_embedding`, `LinkPredictor`, `CountryClassifier` are
   provably the same objects p1 measured. Same Skip-Gram hyper-parameters
   (dim 128, window 5, negative 5, epochs 5, num_walks 10, walk_length 40, workers=1,
   sample=0). That is what makes the combined table a fair comparison.

2. **Schema convention.** A schema string like `UAU` is symmetric (last type == first).
   Its repeating cycle is `schema[:-1]`, so `UAU` -> cycle `UA` -> U,A,U,A,U,...;
   `UUAU` -> cycle `UUA` -> U,U,A,U,U,A,...  This is the standard metapath2vec reading.
   Note `UAUU` and `UUAU` are cyclic rotations of each other and produce the same
   multiset of step types, so running both is pointless — I pick one per cycle class.

3. **Artist start nodes.** `embed_graph` walks from *every* node of H (15,466, users and
   artists). I **rotate the cycle to the start node's type** rather than returning `[]`.
   For `UAU`, an artist start walks A,U,A,U,... — the same meta-path read from the other
   end. For cycle `UUA`, an artist start uses rotation `AUU` -> A,U,U,A,..., which is
   U-U-A-U reversed. This keeps artist vectors trained (they are context for the users)
   and keeps the corpus symmetric. Stated in the answer.

4. **A type-blind control is essential.** `hetero-deepwalk` = p1's plain uniform walk run
   on H. Because a user has ~400 artist neighbours and ~5 social ones, a type-blind walk
   takes a social edge ~1% of the time, so it is *de facto* U-A-U. Comparing it against
   the explicit U-A-U schema isolates "did the meta-path constraint do anything" from
   "did adding artists do anything".

5. **A monotone family, not a grab-bag.** The interesting axis is the fraction of walk
   steps that are social. Cycle `UA` = 0 social, `UUA` = 1/3, `UUUA` = 1/2, and p1's
   DeepWalk on G_train = 1. That is a sweep, and it answers the brief's question
   ("signal or noise?") with a trend instead of two isolated points.

6. **My own idea: rare-artist (IDF) weighting.** Artists are absurdly dense (median 400
   per user). A U-A-U step through a top-1000 artist links two users who share nothing
   but mainstream taste. So on the U->A step draw the artist with probability
   proportional to deg(a)^-alpha (alpha=1), A->U uniform. If density is the problem,
   this should recover some of the loss. This is the "your own ideas" part of the slide.

7. **Three seeds {0,1,2}**, exactly as p1 did, so I inherit a comparable noise floor and
   can say which gaps are real. p1's spread/noise discipline is the right standard and a
   single-seed claim here would be unfalsifiable.

8. **Degree buckets always come from `G_train`**, never H — `evaluate_link_prediction` is
   called with `G_train` as in p1. The cold-start story depends on this: a user with
   social degree 0 may still have hundreds of artists.

## Runs planned

| name | graph | sampler |
|---|---|---|
| (p1) DeepWalk, triadic, ... | G_train | from p1's artefacts, NOT re-run |
| hetero-deepwalk | H_train | uniform, type-blind (control) |
| metapath U-A-U | H_train | cycle UA |
| metapath U-U-A-U | H_train | cycle UUA |
| metapath U-U-U-A-U | H_train | cycle UUUA |
| U-A-U rare-artist a=1 | H_train | cycle UA, U->A weighted deg(a)^-1 |

## Sanity gates before trusting anything

`H_train`: 15,466 nodes; 19,464 + 3,014,361 = 3,033,825 edges; 7,842 artists;
7,624 - 173 = 7,451 users with >= 1 artist. Must match `hetero_stats.json`.
Meta-path walks must be type-correct: assert every sampled walk matches its schema.
