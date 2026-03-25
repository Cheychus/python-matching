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


def create_embeddings():
    model = get_model()

    metadata = []

    idx = 1
    start_total = time.perf_counter()
    for ontology in ONTOLOGIES_LIST:
        embedding_inputs = []
        with open(str(PARSED_DIR / ontology) + ".json") as f:
            terms = json.load(f)

        if EMBEDDING_LIMIT is not None:
            terms = terms[:EMBEDDING_LIMIT]
        for t in terms:
            embedding_inputs.append(t["embedding_input"])
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
        print(f"[EMBEDDING]: {ontology} {idx}/{len(ONTOLOGIES_LIST)}")
        embeddings = model.encode(
            embedding_inputs, batch_size=64, show_progress_bar=True
        )
        np.save(
            str(EMBEDDINGS_DIR / config.SELECTED_MODEL / f"{ontology}_vectors.npy"),
            embeddings,
        )
        idx += 1

    total = time.perf_counter() - start_total
    print(f"[EMBEDDING]: Finished embedding calculation ({total:.2f}s total)")

    with open(str(EMBEDDINGS_DIR / "ontology_metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)
