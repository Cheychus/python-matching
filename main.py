import config
from src.embeddings.similarity_search import load_model
from src.evaluation.evaluate import (
    evaluate_search_method,
    load_and_combine_results,
)
from src.embeddings.create_embeddings import create_embeddings, create_metadata
from src.parser.parse_ontology import parse_ontologies
from src.download.download import download_ontologies
from fuzzywuzzy import fuzz


def setup_pipeline():
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
        create_metadata()

    print("[MAIN]: Pipeline finished")


def evaluation_pipeline():
    ground_truth_a = "ground_truth_talinum.json"
    ground_truth_b = "ground_truth_database.json"

    # evaluate baseline methods
    evaluate_search_method(
        ground_truth_a, method="lexical", method_key="fuzzy", appendix="ground_truth_a"
    )
    evaluate_search_method(
        ground_truth_b, method="lexical", method_key="fuzzy", appendix="ground_truth_b"
    )

    # # with collection
    # evaluate_search_method(
    #     ground_truth,
    #     method="api",
    #     method_key="terminology",
    #     appendix="with_collection_database_truth",
    # )

    # evaluate_search_method(
    #     ground_truth,
    #     method="api",
    #     method_key="tib",
    #     appendix="with_collection_database_truth",
    # )

    # # # without collection
    # evaluate_search_method(
    #     ground_truth,
    #     method="api",
    #     method_key="terminology",
    #     appendix="without_collection_database_truth",
    # )

    # evaluate_search_method(
    #     ground_truth,
    #     method="api",
    #     method_key="tib",
    #     appendix="without_collection_database_truth",
    # )

    # evaluate all models
    # for model in config.MODELS:
    #     config.SELECTED_MODEL = model
    #     load_model(reset=True)
    #     evaluate_search_method(
    #         ground_truth,
    #         method="embedding",
    #         method_key=model.replace("/", "_"),
    #         appendix="ground_truth_b",
    #     )

    # load all json results from the previous evaluation and combine them into csv data
    load_and_combine_results(config.RESULTS_DIR)


def main():
    # run this if cli arguments are passed
    if config.args.download or config.args.parse or config.args.command == "embeddings":
        setup_pipeline()
        return

    # ---- MAIN RUN ----
    # create_metadata()

    # evaluation_pipeline()
    print(fuzz.token_sort_ratio("Gerste", "Barley"))


if __name__ == "__main__":
    config.setup()
    main()
