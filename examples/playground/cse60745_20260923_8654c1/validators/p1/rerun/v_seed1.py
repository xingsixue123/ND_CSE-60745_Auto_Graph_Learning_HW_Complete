from scaffold import RESULTS
from impl import WalkEmbedding
from run_all import BASE, G_train, N_USERS, run_experiment
run_experiment("triadic | seed1", WalkEmbedding(seed=1, **BASE, strategy="triadic"), G_train, N_USERS)
