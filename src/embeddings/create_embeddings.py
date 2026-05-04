import json
import time
import numpy as np
import config
from config import (
    PARSED_DIR,
    EMBEDDINGS_DIR,
    ONTOLOGIES_LIST,
    EMBEDDING_LIMIT,
)
from src.model.embedding_model import get_model


def create_embeddings(save=False):
    model = get_model()

    idx = 1
    start_total = time.perf_counter()
    for ontology in ONTOLOGIES_LIST:
        embedding_inputs = []
        with open(str(PARSED_DIR / ontology) + ".json") as f:
            terms = json.load(f)

        if config.EMBEDDING_LIMIT is not None:
            terms = terms[: config.EMBEDDING_LIMIT]
        for t in terms:
            if config.SELECTED_MODEL == "nomic-ai/nomic-embed-text-v1.5":
                embedding_inputs.append("search_document: " + t["embedding_input"])
            elif config.SELECTED_MODEL == "intfloat/multilingual-e5-large":
                embedding_inputs.append("passage: " + t["embedding_input"])
            else:
                embedding_inputs.append(t["embedding_input"])
        print(f"[EMBEDDING]: {ontology} {idx}/{len(ONTOLOGIES_LIST)}")

        embeddings = model.encode(
            embedding_inputs, batch_size=32, show_progress_bar=False
        )
        if save:
            np.save(
                str(EMBEDDINGS_DIR / config.SELECTED_MODEL / f"{ontology}_vectors.npy"),
                embeddings,
            )
        idx += 1

    total = time.perf_counter() - start_total
    print(f"[EMBEDDING]: Finished embedding calculation ({total:.2f}s total)")


def create_metadata():
    metadata = []
    for ontology in ONTOLOGIES_LIST:
        with open(str(PARSED_DIR / ontology) + ".json") as f:
            terms = json.load(f)
            print(f"{ontology} = {len(terms)} terms")

        if EMBEDDING_LIMIT is not None:
            terms = terms[:EMBEDDING_LIMIT]
        for t in terms:
            metadata.append(
                {
                    "ontology": ontology,
                    "id": t["id"],
                    "short_id": t["short_id"],
                    "label": t["label"],
                    "definition": t["definition"],
                    "synonyms": t["synonyms"],
                    "embedding_input": t["embedding_input"],
                }
            )
    with open(str(EMBEDDINGS_DIR / "ontology_metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)
