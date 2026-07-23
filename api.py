from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.embeddings.similarity_search import (
    api_search,
    load_model,
)
from src.lexical.lexical_search import lexical_search


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root(q: str | None = None, top_k: int = 10, method: str = "embedding"):
    if not q:
        return {"docs": "http://127.0.0.1:8000/docs"}
    if method == "embedding":
        result = api_search(q, top_k)
    elif method == "lexical":
        result = lexical_search(q, top_k)
    return {"q": q, "data": result}
