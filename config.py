from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw_ontologies"
PARSED_DIR = DATA_DIR / "parsed"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"
EVALUATION_DIR = DATA_DIR / "evaluation"
QUERY_DIR = EVALUATION_DIR / "query"

LEVEL = 2
RUN_PIPELINE = False
DOWNLOAD_ONTOLOGIES = False
PARSE_ONTOLOGIES = False
CREATE_EMBEDDINGS = True
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
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",  # 0
    "sentence-transformers/all-MiniLM-L6-v2",  # 1
    "pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb",  # 2
    "jordyvl/scibert_scivocab_uncased_sentence_transformer",  # 3
    "gsarti/scibert-nli",  # 4
]
MODEL_NAME = MODELS[2]
EMBEDDING_LIMIT = 100000  # reduce calculation time, for testing only
# ~50min bei 100.000
TOP_K = 10
