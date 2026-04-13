import csv
import json
from pathlib import Path

from src.api.api_search import api_search
from config import TEST_DIR
import config
from src.embeddings.similarity_search import calculate_similarity, load

GROUND_TRUTH_DIR = TEST_DIR / "ground_truth"
RESULTS_DIR = TEST_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def normalize_id(iri: str):
    return iri.replace("_", ":")


def evaluate_api():
    with open(str(GROUND_TRUTH_DIR) + "/ground_truth_stress.json") as f:
        ground_truth = json.load(f)

    results = []
    for query, truth_value in ground_truth.items():
        print(f"GET API result for {query}...")
        api_results = api_search(query)
        rank = -1
        count = 1
        for r in api_results:
            short_id = normalize_id(r["short_form"])
            if truth_value == short_id:
                rank = count
            count += 1

        top_k_results = [
            {
                "id": normalize_id(r["short_form"]),
                "label": r["label"],
            }
            for r in api_results[: config.TOP_K]
        ]
        hit_1 = rank == 1
        hit_5 = rank != -1 and rank <= 5
        hit_10 = rank != -1 and rank <= 10
        hit_20 = rank != -1 and rank <= 20
        same_label = [r for r in top_k_results if r["label"].lower() == query.lower()]

        results.append(
            {
                "query": query,
                "rank": rank,
                "hit@1": hit_1,
                "hit@5": hit_5,
                "hit@10": hit_10,
                "hit@20": hit_20,
                "reciprocal_rank": 1 / rank if rank > 0 else 0,
                "duplicate_labels": len(same_label) > 1,
                "expected_id": truth_value,
                "top_k_results": top_k_results,
            }
        )
        output = {
            "model": "Terminology API Search",
            "method": "api_search",
            "top_k": config.TOP_K,
            "results": results,
        }

    filename = f"api_k{output['top_k']}.json"
    path = Path(RESULTS_DIR / "api_search")
    path.mkdir(parents=True, exist_ok=True)

    with open(path / filename, "w") as f:
        json.dump(output, f, indent=2)
    json_to_csv(path / filename, str(path) + "/result.csv")
    print("Finished api evaluation")


def evaluate_groundtruth(model_name):
    with open(str(GROUND_TRUTH_DIR) + "/ground_truth_stress.json") as f:
        ground_truth = json.load(f)

    results = []
    for query, truth_value in ground_truth.items():
        result = calculate_similarity(query)
        predictions = result["results"]

        rank = -1
        correct_score = None
        for p in predictions:
            short_id = normalize_id(p["short_id"])
            if truth_value == short_id:
                rank = p["rank"] + 1
                correct_score = p["score"]
                break

        top_k_results = [
            {
                "id": normalize_id(r["short_id"]),
                "label": r["label"],
                "score": r["score"],
            }
            for r in predictions[: config.TOP_K]
        ]
        best_score = predictions[0]["score"] if predictions else None
        same_label = [r for r in top_k_results if r["label"].lower() == query.lower()]

        hit_1 = rank == 1
        hit_5 = rank != -1 and rank <= 5
        hit_10 = rank != -1 and rank <= 10
        hit_20 = rank != -1 and rank <= 20
        # print(f"{query}: rank={rank}, hit@1={hit_1}, hit@5={hit_5}, hit@10={hit_10}")
        results.append(
            {
                "query": query,
                "rank": rank,
                "hit@1": hit_1,
                "hit@5": hit_5,
                "hit@10": hit_10,
                "hit@20": hit_20,
                "reciprocal_rank": 1 / rank if rank > 0 else 0,
                "duplicate_labels": len(same_label) > 1,
                "best_score": best_score,
                "correct_score": correct_score,
                "expected_id": truth_value,
                "top_k_results": top_k_results,
            }
        )
        output = {
            "model": model_name,
            "method": "embedding",
            "top_k": config.TOP_K,
            "results": results,
        }

    filename = f"embedding_k{output['top_k']}.json"
    path = Path(RESULTS_DIR / str(output["model"]))
    path.mkdir(parents=True, exist_ok=True)

    with open(path / filename, "w") as f:
        json.dump(output, f, indent=2)
    json_to_csv(path / filename, str(path) + "/result.csv")
    print("Finished evaluation")


def json_to_csv(json_path, csv_path):
    with open(json_path) as f:
        data = json.load(f)

    model = data["model"]
    method = data["method"]
    top_k = data["top_k"]

    rows = []

    for r in data["results"]:
        row = {
            "model": model,
            "method": method,
            "top_k": top_k,
            "query": r["query"],
            "rank": r["rank"],
            "hit@1": int(r["hit@1"]),
            "hit@5": int(r["hit@5"]),
            "hit@10": int(r["hit@10"]),
        }
        rows.append(row)

    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
