from src.api.api_search import api_search
import config
from src.evaluation.evaluate import evaluate_api, evaluate_groundtruth, evaluate_lexical
from src.embeddings.create_embeddings import create_embeddings
from src.embeddings.similarity_search import (
    load,
    search,
)
from src.parser.parse_ontology import parse_ontologies
from src.download.download import download_ontologies
from src.lexical.lexical_search import lexical_search


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
        # load()
        # for model in config.MODELS:
        #     config.SELECTED_MODEL = model
        #     load(reset=True)
        # evaluate_groundtruth(config.SELECTED_MODEL)

        # evaluate_api()
        # result = api_search("organism")
        # print(result)
        # results = lexical_search("organism", 20)
        # print(results)
        # results = lexical_search("hordeum", 20)
        print("Finished custom run")
    # evaluate_lexical()

    # manual search
    # search("function")
    # search("organism")
    # search("mouse")
    # search("Hordeum vulgare")
    # search("Soil")
    # search("Plant")
    # search("Live")
    # search("Cell")


if __name__ == "__main__":
    config.setup()
    main()
