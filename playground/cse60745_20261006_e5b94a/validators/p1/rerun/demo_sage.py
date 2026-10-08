"""Step 1: run the GraphSAGE demo (notebook cell 13) end to end, as cell 12 instructs,
so that any later failure is mine and not the framework's. Also builds the node2vec cache."""
import json
from common import MySAGEConv, train_and_eval

best = train_and_eval("GraphSAGE", MySAGEConv)
json.dump(best, open("logs/result_sage.json", "w"), indent=2)
