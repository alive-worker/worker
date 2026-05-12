from fastapi import FastAPI

from app.db import init_db
from app.api import notes, tags, search, export

app = FastAPI(title="notebox", version="0.1.0")


@app.on_event("startup")
def _startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(notes.router)
app.include_router(tags.router)
app.include_router(search.router)
app.include_router(export.router)
