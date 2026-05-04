from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.embeddings.similarity_search import (
    api_search,
    load_model,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root(q: str | None = None, top_k: int = 10):
    if not q:
        return {"docs": "http://127.0.0.1:8000/docs"}
    result = api_search(q, top_k)
    return {"q": q, "data": result}
