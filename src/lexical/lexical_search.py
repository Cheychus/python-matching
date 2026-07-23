import json
import time

from config import EMBEDDINGS_DIR
from rapidfuzz import fuzz

metadata = None


def get_terms(entry):
    terms = entry[entry["label"]]
    terms.extend(entry.get("synonyms", []))
    return terms


def load_metadata():
    global metadata
    with open(str(EMBEDDINGS_DIR / "ontology_metadata.json")) as f:
        metadata = json.load(f)

    for m in metadata:
        m["label"] = m["label"].lower()
        for syn in m.get("synonyms", []):
            syn = syn.lower()


def fuzzy_score(query, text):
    return fuzz.token_sort_ratio(query, text)


def lexical_search(query: str, top_k=10):
    if not metadata:
        load_metadata()

    startTime = time.perf_counter()
    query_norm = query.lower()

    grouped = {}

    for m in metadata:
        concept_id = m["id"]

        best_score = fuzzy_score(query_norm, m["label"])

        for syn in m.get("synonyms", []):
            score = fuzzy_score(query_norm, syn.lower())
            best_score = max(best_score, score)

        if concept_id not in grouped:
            grouped[concept_id] = {
                "id": concept_id,
                "short_form": m["short_id"],
                "label": m["label"],
                "definition": m["definition"],
                "embedding_input": m["embedding_input"],
                "ontologies": [],
                "score": best_score,
            }

        grouped[concept_id]["ontologies"].append(m["ontology"])
        grouped[concept_id]["score"] = max(grouped[concept_id]["score"], best_score)

    # --- ranking ---
    results = list(grouped.values())
    results.sort(key=lambda x: x["score"], reverse=True)

    final_results = results[:top_k]

    for idx, r in enumerate(final_results):
        r["rank"] = idx

    result = {
        "query": query,
        "results": final_results,
        "runtime_ms": (time.perf_counter() - startTime) * 1000,
        "model": "rapidfuzz_lexical",
    }

    return result
