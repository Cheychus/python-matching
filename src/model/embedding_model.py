from sentence_transformers import SentenceTransformer
import config
import torch

_loaded_model = None


def get_device():
    print("[MODEL]: loading embedding model")
    print("Torch Version: ", torch.__version__)
    print("CUDA available: ", torch.cuda.is_available())
    device = "cuda" if torch.cuda.is_available() and config.DEVICE == "gpu" else "cpu"
    if device == "cuda":
        print("Using GPU:", torch.cuda.get_device_name(0))
    else:
        print("Using CPU")
    return device


def get_model(reset=False):
    global _loaded_model

    if _loaded_model is None or reset:
        device = get_device()

        if config.SELECTED_MODEL == "nvidia/llama-embed-nemotron-8b":
            attn_implementation = "eager"  # Or "flash_attention_2"
            _loaded_model = SentenceTransformer(
                config.SELECTED_MODEL,
                trust_remote_code=True,
                model_kwargs={
                    "attn_implementation": attn_implementation,
                    "torch_dtype": "bfloat16",
                },
                processor_kwargs={"padding_side": "left"},
                device=device,
            )
        elif config.SELECTED_MODEL == "Qwen/Qwen3-Embedding-0.6B":
            _loaded_model = SentenceTransformer(
                config.SELECTED_MODEL,
                model_kwargs={
                    "attn_implementation": "flash_attention_2",
                    "device_map": "auto",
                },
                processor_kwargs={"padding_side": "left"},
                device=device,
            )
        else:
            _loaded_model = SentenceTransformer(
                config.SELECTED_MODEL, device=device, trust_remote_code=False
            )

    return _loaded_model
