from sentence_transformers import SentenceTransformer
import config

_model = None


def get_model():

    global _model

    if _model is None:
        print("[MODEL]: loading embedding model")
        _model = SentenceTransformer(config.MODEL_NAME)

    return _model
