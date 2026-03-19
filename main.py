from pathlib import Path
from fastapi import FastAPI

import config
from multiprocessing import Pool
from tqdm import tqdm
from src.embeddings.create_embeddings import create_embeddings
from src.embeddings.similarity_search import (
    api_search,
    calculate_similarity,
    load,
    search,
)
from src.parser.parse_ontology import parse_ontologies
from src.download.download import download_ontologies

config.RAW_DIR.mkdir(parents=True, exist_ok=True)
config.PARSED_DIR.mkdir(parents=True, exist_ok=True)
config.EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)
for model in config.MODELS:
    Path(config.QUERY_DIR / model).mkdir(parents=True, exist_ok=True)
    Path(config.EMBEDDINGS_DIR / model).mkdir(parents=True, exist_ok=True)


if not config.RUN_PIPELINE:
    app = FastAPI()
    load()

    @app.get("/")
    def read_root(q: str | None = None, top_k: int = 10):
        if not q:
            return {"docs": "http://127.0.0.1:8000/docs"}
        result = api_search(q, top_k)
        return {"q": q, "data": result}


def pipeline():
    print("[MAIN]: Start Pipeline")
    if config.DOWNLOAD_ONTOLOGIES:
        print("[MAIN]: Download ontologies")
        download_ontologies()

    if config.PARSE_ONTOLOGIES:
        print("[MAIN]: Parse ontologies. This may take some minutes (~30min)")
        parse_ontologies()

    if config.CREATE_EMBEDDINGS:
        print(
            "[MAIN]: Create embeddings. This may take some minutes or even hours. Please wait..."
        )
        create_embeddings()

    print("[MAIN]: Pipeline finished")


def main():
    if config.RUN_PIPELINE:
        pipeline()
        return
    else:
        print("[MAIN]: Skipped Pipeline")

    load()

    search("function")
    search("organism")
    search("mouse")
    search("Hordeum vulgare")
    search("Soil")
    search("Plant")
    search("Live")
    search("Cell")


if __name__ == "__main__":
    main()
