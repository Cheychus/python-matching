import config
from src.embeddings.create_embeddings import create_embeddings
from src.embeddings.similarity_search import (
    load,
    search,
)
from src.parser.parse_ontology import parse_ontologies
from src.download.download import download_ontologies


def pipeline():
    print("[MAIN]: Start Pipeline")
    if config.args.download:
        print("[MAIN]: Download ontologies")
        download_ontologies()

    if config.args.parse:
        print("[MAIN]: Parse ontologies. This may take some minutes (~30min)")
        parse_ontologies()

    if config.args.command == "embeddings":
        print(
            "[MAIN]: Create embeddings. This may take some minutes or even hours. Please wait..."
        )
        create_embeddings()

    print("[MAIN]: Pipeline finished")


def main():
    if config.args.download or config.args.parse or config.args.command == "embeddings":
        pipeline()
    else:
        load()

        # manual search
        search("function")
        search("organism")
        search("mouse")
        search("Hordeum vulgare")
        search("Soil")
        search("Plant")
        search("Live")
        search("Cell")


if __name__ == "__main__":
    config.setup()
    main()
