import json
import numpy as np
from sentence_transformers import SentenceTransformer
from config import MODEL_NAME, PARSED_DIR, EMBEDDINGS_DIR, ONTOLOGIES_LIST
from src.model.embedding_model import get_model


def createEmbeddings():
    model = get_model()
    allTexts = []
    metadata = []

    for ontology in ONTOLOGIES_LIST:
        with open(str(PARSED_DIR / ontology) + ".json") as f:
            terms = json.load(f)
        for t in terms:
            allTexts.append(t["embeddingInput"])
            metadata.append({"ontology": ontology, "id": t["id"], "label": t["label"]})

    embeddings = model.encode(allTexts, batch_size=64, show_progress_bar=True)

    np.save(str(EMBEDDINGS_DIR / "ontology_vectors.npy"), embeddings)

    with open(str(EMBEDDINGS_DIR / "ontologyMetadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)
