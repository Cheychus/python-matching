import time

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
from config import EMBEDDINGS_DIR, ONTOLOGIES_LIST, PARSED_DIR
from src.model.embedding_model import get_model

vectors = None
metadata = None
model = None


def load():
    global vectors, metadata, model
    model = get_model()
    path = str(EMBEDDINGS_DIR / "ontology_vectors.npy")
    vectors = np.load(path)
    with open(str(EMBEDDINGS_DIR / "ontologyMetadata.json")) as f:
        metadata = json.load(f)


def calculateSimilarity(value: str, ontology="BFO"):
    embedding = model.encode(value)
    scores = cosine_similarity([embedding], vectors)[0]
    top = np.argsort(scores)[-5:][::-1]

    result = ""

    for i in top:
        m = metadata[i]
        result += (
            str(m["ontology"])
            + " "
            + str(m["id"])
            + " "
            + str(m["label"])
            + " "
            + str(scores[i])
            + "\n"
        )
        # print(m["ontology"], m["id"], m["label"], scores[i])

    return result


def search(value):
    startTime = time.perf_counter()
    result = calculateSimilarity(value)
    endTime = time.perf_counter()
    elapsed = endTime - startTime
    print("Search: ", value, "\n Result: \n", result)
    print("Runtime: ", elapsed * 1000, "ms")
