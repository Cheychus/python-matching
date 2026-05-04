import glob
import json
from pathlib import Path
import pandas as pd
import config
import matplotlib.pyplot as plt


def load_results(results_dir):
    rows = []

    for file in Path(results_dir).rglob("*.json"):
        if "k20" not in file.name:
            continue
        with open(file) as f:
            data = json.load(f)

        for r in data["results"]:
            rows.append(
                {
                    "model": data["model"],
                    "method": data["method"],
                    "top_k": data["top_k"],
                    "query": r["query"],
                    "rank": r["rank"],
                    "hit@1": int(r["hit@1"]),
                    "hit@5": int(r["hit@5"]),
                    "hit@10": int(r["hit@10"]),
                    "hit@20": int(r["hit@20"]),
                }
            )

    return pd.DataFrame(rows)


def generate_results(df):
    df.groupby("model")["hit@1"].mean().plot(kind="bar")
    plt.ylabel("Hit@1")
    plt.savefig("hit1_per_model.png")
    plt.axes.autoscale()

    pivot = df.groupby("model")[["hit@1", "hit@5", "hit@10"]].mean()
    pivot.plot(kind="bar")
    plt.savefig("comparison.png")


def results_pipeline():
    df = load_results(config.RESULTS_DIR)
    generate_results(df)
