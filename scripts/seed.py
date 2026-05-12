"""Populate the database with sample notes for local exploration."""
from app.db import init_db, session_scope
from app.models import Note, Tag


SAMPLES = [
    {
        "title": "FastAPI dependency injection cheatsheet",
        "body": (
            "FastAPI's Depends() resolves a callable per request. Use it for "
            "database sessions, auth principals, and pagination params. "
            "Sub-dependencies are cached within the same request."
        ),
        "tags": ["python", "fastapi", "cheatsheet"],
    },
    {
        "title": "SQLite WAL mode notes",
        "body": (
            "Enable WAL with `PRAGMA journal_mode=WAL`. Improves concurrent "
            "reads while a write transaction is open. Beware of the -wal and "
            "-shm sidecar files when backing up."
        ),
        "tags": ["sqlite", "ops"],
    },
    {
        "title": "Docker multi-stage build pattern",
        "body": (
            "Use a builder stage to install build tools and compile wheels, "
            "then COPY only the resulting site-packages into the runtime "
            "image. Cuts image size dramatically for Python services."
        ),
        "tags": ["docker", "devops", "python"],
    },
    {
        "title": "Pydantic v2 migration gotchas",
        "body": (
            "orm_mode is now from_attributes. Validators use @field_validator. "
            "BaseSettings moved to pydantic-settings. Most .dict() calls "
            "become .model_dump()."
        ),
        "tags": ["python", "pydantic", "cheatsheet"],
    },
    {
        "title": "Reading list: distributed systems",
        "body": (
            "- Designing Data-Intensive Applications\n"
            "- Database Internals\n"
            "- Site Reliability Engineering\n"
            "Skim the chapters on consistency models first."
        ),
        "tags": ["reading", "distributed-systems"],
    },
]


def run() -> None:
    init_db()
    with session_scope() as db:
        if db.query(Note).first():
            print("notes already present; skipping seed")
            return
        tag_cache: dict[str, Tag] = {}
        for entry in SAMPLES:
            note = Note(title=entry["title"], body=entry["body"])
            for raw in entry["tags"]:
                name = raw.lower()
                tag = tag_cache.get(name)
                if tag is None:
                    tag = Tag(name=name)
                    db.add(tag)
                    tag_cache[name] = tag
                note.tags.append(tag)
            db.add(note)
    print(f"seeded {len(SAMPLES)} notes")


if __name__ == "__main__":
    run()
