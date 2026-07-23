import csv
import json
from pathlib import Path
import time

import pandas as pd

from src.lexical.lexical_search import lexical_search
from src.api.api_search import api_search
from config import TEST_DIR
import config
from src.embeddings.similarity_search import calculate_similarity

GROUND_TRUTH_DIR = TEST_DIR / "ground_truth"
RESULTS_DIR = TEST_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def normalize_id(iri: str):
    return iri.replace("_", ":")


def evaluate_search_method(
    ground_truth: str, method="api", method_key="terminology", appendix="standard"
):
    with open(GROUND_TRUTH_DIR / ground_truth) as f:
        ground_truth_json = json.load(f)

    querycount = 1
    data = []

    for query, truth_value in ground_truth_json.items():
        print(
            f"Get Results for: {query} ({querycount}/{len(ground_truth_json.items())})"
        )
        querycount += 1
        start = time.perf_counter()

        if method == "api":
            collection = False if "without_collection" in appendix else True
            results = api_search(query, method_key, collection)
        elif method == "embedding":
            results = calculate_similarity(query)["results"]
        elif method == "lexical":
            results = lexical_search(query, top_k=config.TOP_K)["results"]
        else:
            print(f"Unsupported search method {method} {method_key}")
            return

        elapsed = time.perf_counter() - start
        rank = -1  # if truth term not found, rank = -1
        rankcount = 1
        score = -1
        best_score = -1
        hit_score = None
        for r in results:
            score = r.get("score")
            best_score = max(best_score, score)

            short_id = normalize_id(r["short_form"])
            if truth_value == short_id:
                rank = rankcount
                hit_score = score
                break
            rankcount += 1

        # save topk results
        topk_results = [
            {
                "id": normalize_id(r["short_form"]),
                "label": r["label"],
                "score": r.get("score"),
            }
            for r in results[: config.TOP_K]
        ]

        hit_1 = rank == 1
        hit_5 = rank != -1 and rank <= 5
        hit_10 = rank != -1 and rank <= 10
        hit_20 = (
            rank != -1 and rank <= 20
        )  # probably unneccessary, but good for evaluation
        same_label = [
            r for r in topk_results if getattr(r, "label", "").lower() == query.lower()
        ]  # useful to identify results, where the query exactly matches the truth term

        data.append(
            {
                "query": query,
                "time_ms": elapsed * 1000,
                "rank": rank,
                "hit@1": hit_1,
                "hit@5": hit_5,
                "hit@10": hit_10,
                "hit@20": hit_20,
                "score": hit_score,
                "best_score": best_score,
                "reciprocal_rank": 1 / rank if rank > 0 else 0,
                "duplicate_labels": len(same_label) > 1,
                "expected_id": truth_value,
                "top_k_results": topk_results,
            }
        )

    # Output for results json file
    output = {
        "method": method,  # search method: api, embedding, lexical
        "method_key": method_key,  # Terminology, Tib, Embedding Model oder Fuzzy Matching Method
        "appendix": appendix,  # extra information for custom runs, default = standard
        "top_k": config.TOP_K,  # the configurated top k setting
        "results": data,  # result data
    }

    # save results as json file
    filename = f"{method}_k{output['top_k']}_{appendix}_{ground_truth}"
    path = Path(RESULTS_DIR / method / method_key)
    path.mkdir(parents=True, exist_ok=True)

    with open(path / filename, "w") as f:
        json.dump(output, f, indent=2)

    # convert json data to csv data for excel analysis
    json_to_csv(path / filename, str(path) + "/result.csv")

    print(f"Finished {method}_{method_key} evaluation")


def json_to_csv(json_path, csv_path):
    with open(json_path) as f:
        data = json.load(f)

    rows = []

    for r in data["results"]:
        row = {
            "method": data["method"],
            "method_key": data["method_key"],
            "appendix": data["appendix"],
            "top_k": data["top_k"],
            "query": r["query"],
            "rank": r["rank"],
            "hit@1": int(r["hit@1"]),
            "hit@5": int(r["hit@5"]),
            "hit@10": int(r["hit@10"]),
            "hit@20": int(r["hit@20"]),
            "reciprocal_rank": r["reciprocal_rank"],
            "duplicate_labels": r["duplicate_labels"],
            "expected_id": r["expected_id"],
        }
        rows.append(row)

    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def compute_metrics(df):
    grouped = df.groupby("method_key")

    summary = pd.DataFrame(
        {
            "MRR": grouped["reciprocal_rank"].mean(),
            "Hit@1": grouped["hit@1"].mean(),
            "Hit@5": grouped["hit@5"].mean(),
            "Hit@10": grouped["hit@10"].mean(),
            "Avg_Rank": grouped["rank"].mean(),
            "Median_Rank": grouped["rank"].median(),
            "Avg_Time_ms": grouped["time_ms"].mean(),
            "Avg_Num_Results": grouped["num_results"].mean(),
        }
    )

    return summary.reset_index()


def load_and_combine_results(json_folder_path):
    all_rows = []
    files = Path(json_folder_path).rglob("*.json")

    print(files)
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        method = data.get("method")
        method_key = data.get("method_key")

        for r in data["results"]:
            row = {
                "method": method,
                "method_key": method_key,
                "appendix": data.get("appendix"),
                "query": r.get("query"),
                "expected_id": r.get("expected_id"),
                "rank": r.get("rank"),
                "hit@1": int(r.get("hit@1", False)),
                "hit@5": int(r.get("hit@5", False)),
                "hit@10": int(r.get("hit@10", False)),
                "hit@20": int(r.get("hit@20", False)),
                "reciprocal_rank": r.get("reciprocal_rank"),
                "time_ms": r.get("time_ms"),
                "duplicate_labels": r.get("duplicate_labels"),
                "num_results": len(r.get("top_k_results", [])),
            }

            all_rows.append(row)

    df = pd.DataFrame(all_rows)
    summary_df = compute_metrics(df)
    df.to_csv(json_folder_path / "combined_results.csv", index=False)
    summary_df.to_csv(json_folder_path / "summary_metrics.csv", index=False)

    print("Generated CSV Data")
