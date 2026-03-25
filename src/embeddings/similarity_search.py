import time
import numpy as np
import json
from config import (
    EMBEDDINGS_DIR,
    QUERY_DIR,
    SELECTED_MODEL,
    TOP_K,
    ONTOLOGIES_LIST,
)
from src.model.embedding_model import get_model

vectors = None
metadata = None
model = None


def load():
    global vectors, metadata, model
    model = get_model()
    all_vectors = []

    for ontology in ONTOLOGIES_LIST:
        vectorpath = str(EMBEDDINGS_DIR / SELECTED_MODEL / f"{ontology}_vectors.npy")
        vecs = np.load(vectorpath)
        all_vectors.append(vecs)

    with open(str(EMBEDDINGS_DIR / "ontology_metadata.json")) as f:
        metadata = json.load(f)

    vectors = np.vstack(all_vectors)
    vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)  # skalarprodukt

    assert len(metadata) == len(vectors)  # needs to be same length


def calculate_similarity(value: str, top_k=TOP_K):
    embedding = model.encode(value)
    embedding = embedding / np.linalg.norm(embedding)
    scores = np.dot(vectors, embedding)
    top = np.argpartition(scores, -50)[-50:]
    top = top[np.argsort(scores[top])[::-1]]

    grouped = {}
    result = {"query": value, "results": []}

    for i in top:
        m = metadata[i]
        concept_id = m["id"]

        if concept_id not in grouped:
            grouped[concept_id] = {
                "id": concept_id,
                "short_id": m["short_id"],
                "label": m["label"],
                "definition": m["definition"],
                "embedding_input": m["embedding_input"],
                "ontologies": [],
                "score": float(scores[i]),
            }

        grouped[concept_id]["ontologies"].append(m["ontology"])
        grouped[concept_id]["score"] = max(
            grouped[concept_id]["score"], float(scores[i])
        )

    results = list(grouped.values())
    results.sort(key=lambda x: x["score"], reverse=True)
    final_results = results[:top_k]
    for idx, r in enumerate(final_results):
        r["rank"] = idx
    result["results"] = final_results
    return result


def search(value: str):
    startTime = time.perf_counter()
    result = calculate_similarity(value)
    result["runtime_ms"] = (time.perf_counter() - startTime) * 1000
    result["model"] = SELECTED_MODEL

    filename = value.lower() + ".json"
    with open(str(QUERY_DIR / SELECTED_MODEL / filename), "w") as f:
        json.dump(result, f, indent=2)

    return result


def api_search(query: str, top_k: int):
    result = calculate_similarity(query, top_k)
    return result
