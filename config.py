from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw_ontologies"
PARSED_DIR = DATA_DIR / "parsed"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"

LEVEL = 2
RUN_PIPELINE = True
DOWNLOAD_ONTOLOGIES = False
PARSE_ONTOLOGIES = False
CREATE_EMBEDDINGS = True
ONTOLOGIES_LIST = ["BFO" , "COB", "DPBO", "PPEO", "PCO", "UO", "BCO", "RO", "PPO", "MSIO", "PECO", "MMO", "STATO", "SWO", "TO", "EDAM","OMP", "MS", "PO", "CHMO", "AGRO", "PSO", "OBI", "ENVO", "MOD", "BAO", "BTO", "PATO", "FLOPO", "UBERON", "GO", "EFO", "CHEBI", "NCIT"]


MODELS = [
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    "sentence-transformers/all-MiniLM-L6-v2",
]
MODEL_NAME = MODELS[1]
TOP_K = 5
