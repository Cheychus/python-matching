import json
import pandas as pd
from pathlib import Path


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


def compute_metrics(df):
    df["mrr"] = df["rank"].apply(lambda r: 1 / r if r > 0 else 0)

    metrics = df.groupby("model")[["hit@1", "hit@5", "hit@10", "mrr"]].mean()

    return metrics


def create_pivot(df):
    pivot = df.pivot_table(index="query", columns="model", values="hit@5")

    return pivot.fillna(0).astype(int)


import matplotlib.pyplot as plt


def plot_metrics(metrics, output_dir):
    metrics.plot(kind="bar")
    plt.title("Model Comparison")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_dir / "metrics.png")
    plt.close()


def main():
    results_dir = Path("results")
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # 1. Laden
    df = load_results(results_dir)

    # 2. Speichern (roh)
    df.to_csv(output_dir / "merged.csv", index=False)

    # 3. Metrics
    metrics = compute_metrics(df)
    metrics.to_csv(output_dir / "metrics.csv")

    # 4. Pivot
    pivot = create_pivot(df)
    pivot.to_csv(output_dir / "pivot.csv")

    # 5. Plot
    plot_metrics(metrics, output_dir)

    print("Evaluation fertig.")


main()
