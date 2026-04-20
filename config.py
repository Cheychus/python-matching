from pathlib import Path
import config
import argparse

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw_ontologies"
PARSED_DIR = DATA_DIR / "parsed"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"
EVALUATION_DIR = DATA_DIR / "evaluation"
QUERY_DIR = EVALUATION_DIR / "query"
TEST_DIR = BASE_DIR / "tests"

ONTOLOGIES_LIST = [
    "BAO",
    "BFO",
    "COB",
    "DPBO",
    "PPEO",
    "PCO",
    "UO",
    "BCO",
    "RO",
    "PPO",
    "MSIO",
    "PECO",
    "MMO",
    "STATO",
    "SWO",
    "TO",
    "EDAM",
    "OMP",
    "MS",
    "PO",
    "CHMO",
    "AGRO",
    "PSO",
    "OBI",
    "ENVO",
    "MOD",
    "BAO",
    "BTO",
    "PATO",
    "FLOPO",
    "UBERON",
    "GO",
    "EFO",
    "CHEBI",
    "NCIT",
]

MODELS = [
    # most download
    "sentence-transformers/all-MiniLM-L6-v2",  # 0
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",  # 1
    "sentence-transformers/all-mpnet-base-v2",  # 2,
    # "cross-encoder/ms-marco-MiniLM-L6-v2", nicht nutzbar, cross encoder, kein model.encode moeglich
    "BAAI/bge-small-en-v1.5",  # 3
    "BAAI/bge-m3",  # 4
    "nomic-ai/nomic-embed-text-v1.5",  # 5 (search_document: ..., search_query: ...) -> model.encode()
    "BAAI/bge-large-en-v1.5",  # 6
    # "BAAI/bge-reranker-v2-m3" reranker modell, ungeeignet fuer BA
    "BAAI/bge-base-en-v1.5",  # 7
    "intfloat/multilingual-e5-large",  # 8 (query: ..., passage: ...)
    #  "Qwen/Qwen3-Embedding-0.6B",  # 9 dauert zu lange!
    # "nomic-ai/nomic-embed-text-v1" aeltere version
    # "intfloat/multilingual-e5-small", # 10 small modell von intfloat
    "pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb",  # 10 domain specific
    "pritamdeka/S-Scibert-snli-multinli-stsb",  # 11 domain
    "sentence-transformers/allenai-specter",  # 12 domain
    "NeuML/pubmedbert-base-embeddings",  # 13 domain
    #  "nvidia/llama-embed-nemotron-8b",  # 14 ols search model, dauert zu lange!
    #  "nvidia/llama-nemotron-embed-1b-v2",  # 15 kleineres ols model, dauert auch zu lange
]

# MODELS = [
#     "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",  # 0
#     "sentence-transformers/all-MiniLM-L6-v2",  # 1
#     "pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb",  # 2
#     "jordyvl/scibert_scivocab_uncased_sentence_transformer",  # 3
#     "thuan9889/llama_embedding_model_v1",  # 4
#     "Trelis/all-MiniLM-L12-v2-ft-Llama-3-70B",  # 5
#     "BAAI/bge-large-en-v1.5",  # 6 ~22min bei Limit 1000
#     "BAAI/bge-small-en-v1.5",  # 7
#     "BAAI/bge-base-en-v1.5",  # 8
#     "intfloat/multilingual-e5-large",  # 9
#     "intfloat/multilingual-e5-small",  # 10
#     # "perplexity-ai/pplx-embed-v1-0.6b",  # 11 ~41min limit = 1000
#     # "nvidia/llama-embed-nemotron-8b",  # 12
# ]
args = None
SELECTED_MODEL: str = MODELS[
    7
]  # Select API Model here and model for testing with main()
DEVICE: str = "gpu"  # cpu | gpu
EMBEDDING_LIMIT: None | int = 100  # reduce calculation time, for testing only
# ~50min bei 100.000
TOP_K = 20


def setup_directories():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PARSED_DIR.mkdir(parents=True, exist_ok=True)
    EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)
    for model in MODELS:
        Path(QUERY_DIR / model).mkdir(parents=True, exist_ok=True)
        Path(EMBEDDINGS_DIR / model).mkdir(parents=True, exist_ok=True)


def setup():
    global args, SELECTED_MODEL, DEVICE

    setup_directories()

    parser = argparse.ArgumentParser(
        prog="PYTHON ONTOLOGY MATCHING SERVICE",
        description="This python tool will download, parse and create embeddings based from a list of specified ontologies. First download and parse the ontologies with python main.py -d -p and after that, create embeddings for the specified models with python main.py embeddings [0,1,2,3,4] -d cpu | gpu",
    )
    subparsers = parser.add_subparsers(dest="command")
    emb_parser = subparsers.add_parser("embeddings")

    emb_parser.add_argument(
        "model",
        help="Choose a sentence transformer model from the specified config list",
        type=int,
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        default=2,
    )
    emb_parser.add_argument(
        "-d",
        "--device",
        help="You can either calculate embeddings on cpu or gpu. GPU may be faster. CPU is standard",
        choices=["cpu", "gpu"],
        default="cpu",
    )
    parser.add_argument(
        "-d",
        "--download",
        help="Download all ontologies specified in the ontologies list.",
        action="store_true",
    )
    parser.add_argument(
        "-p",
        "--parse",
        help="Parse all ontologies from the specified ontologies list",
        action="store_true",
    )

    args = parser.parse_args()
    if args.command == "embeddings":
        config.SELECTED_MODEL = MODELS[args.model]  # overwrite config default model
        config.DEVICE = args.device
