from sentence_transformers import SentenceTransformer
import config
import torch

_model = None


def get_model():
    print(torch.__version__)
    print(torch.cuda.is_available())
    print(torch.version.cuda)
    print(torch.cuda.get_device_name(0))

    global _model

    if _model is None:
        print("[MODEL]: loading embedding model")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print("Using device: ", device)
        _model = SentenceTransformer(config.MODEL_NAME, device="cpu")

    return _model
