from sentence_transformers import SentenceTransformer
import config
import torch

_loaded_model = None


def get_model():
    global _loaded_model

    if _loaded_model is None:
        print("[MODEL]: loading embedding model")
        print("Torch Version: ", torch.__version__)
        print("CUDA available: ", torch.cuda.is_available())
        print("GPU Device: ", torch.cuda.get_device_name(0))

        device = (
            "cuda" if torch.cuda.is_available() and config.DEVICE == "gpu" else "cpu"
        )
        print("Using device: ", device)
        _loaded_model = SentenceTransformer(config.SELECTED_MODEL, device=device)

    return _loaded_model
