"""Control: feed the pipeline a random embedding. If the evaluation path is sound,
link prediction must collapse to chance (hit@1 = 1/21 = 0.0476, MRR = 0.1736) and
country classification to roughly the majority-class rate."""
import numpy as np
from scaffold import load_data, evaluate_link_prediction, evaluate_country
from impl import LinkPredictor, CountryClassifier

G, splits, country, csplit, N = load_data()
rng = np.random.default_rng(0)
Z = rng.normal(size=(N, 128))
lp = evaluate_link_prediction(Z, LinkPredictor(), splits, G)
cc = evaluate_country(Z, country, CountryClassifier(), csplit)
print("random-Z  LP val", lp["val"][0], "\nrandom-Z  LP test", lp["test"][0])
print("random-Z  country\n", cc)
maj = np.bincount(country).max() / len(country)
print(f"chance hit@1 {1/21:.4f}  chance MRR {sum(1/k for k in range(1,22))/21:.4f}  majority-class rate {maj:.4f}")
