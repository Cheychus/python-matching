import time

import config
from multiprocessing import Pool
from tqdm import tqdm
from src.embeddings.create_embeddings import createEmbeddings
from src.embeddings.similarity_search import calculateSimilarity, load, search
from src.parser.parse_ontology import parseOntologies
from src.download.download import downloadOntologies
from config import (
    ONTOLOGIES_LIST,
    RUN_PIPELINE,
    DOWNLOAD_ONTOLOGIES,
    PARSE_ONTOLOGIES,
    CREATE_EMBEDDINGS,
)

config.RAW_DIR.mkdir(parents=True, exist_ok=True)
config.PARSED_DIR.mkdir(parents=True, exist_ok=True)
config.EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)


def pipeline():
    print("[MAIN]: Start Pipeline")
    if DOWNLOAD_ONTOLOGIES:
        print("[MAIN]: Download ontologies")
        downloadOntologies()

    if PARSE_ONTOLOGIES:
        print("[MAIN]: Parse ontologies. This may take some minutes...")
        parseOntologies()
    
    if CREATE_EMBEDDINGS:
        print("[MAIN]: Create embeddings. This may take some minutes or even hours. Please wait...")
        createEmbeddings()

    print("[MAIN]: Pipeline finished")


def main():
    if RUN_PIPELINE:
        pipeline()
    else:
        print("[MAIN]: Skipped Pipeline")

    return 
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
