import json
import numpy as np
from config import (
    MODEL_NAME,
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
    for ontology in ONTOLOGIES_LIST:
        embedding_inputs = []
        with open(str(PARSED_DIR / ontology) + ".json") as f:
            terms = json.load(f)

        
        for t in terms[:EMBEDDING_LIMIT]:
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
            str(EMBEDDINGS_DIR / MODEL_NAME / f"{ontology}_vectors.npy"),
            embeddings,
        )
        idx += 1

    with open(str(EMBEDDINGS_DIR / "ontology_metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)
