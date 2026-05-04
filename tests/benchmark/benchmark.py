import time
import statistics
import config
from src.embeddings.create_embeddings import create_embeddings
from src.model.embedding_model import get_model


def benchmark_model(model: str, limit=1, runs=10):
    times = []

    config.SELECTED_MODEL = model
    config.EMBEDDING_LIMIT = limit
    config.SELECTED_MODEL = model
    get_model(True)

    for _ in range(runs):
        start = time.perf_counter()
        create_embeddings()
        end = time.perf_counter()

        times.append(end - start)

    return {
        "model": model,
        "mean": statistics.mean(times),
        "std": statistics.stdev(times),
        "min": min(times),
        "max": max(times),
    }
