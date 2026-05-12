from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Note
from app.schemas import SearchHit


SNIPPET_RADIUS = 40


def _score(text: str, term: str) -> float:
    if not text:
        return 0.0
    return float(text.lower().count(term.lower()))


def _snippet(body: str, term: str) -> str:
    lower = body.lower()
    idx = lower.find(term.lower())
    if idx == -1:
        return body[:SNIPPET_RADIUS * 2].strip()
    start = max(0, idx - SNIPPET_RADIUS)
    end = min(len(body), idx + len(term) + SNIPPET_RADIUS)
    prefix = "..." if start > 0 else ""
    suffix = "..." if end < len(body) else ""
    return f"{prefix}{body[start:end].strip()}{suffix}"


def keyword_search(db: Session, term: str, *, limit: int = 20) -> list[SearchHit]:
    """Naive LIKE-based search across notes.

    Known limitation: scans every note row and computes scores in Python. Fine
    for hundreds of rows; would need FTS for large corpora.
    """
    pattern = f"%{term}%"
    rows = (
        db.execute(
            select(Note).where(
                (Note.title.ilike(pattern)) | (Note.body.ilike(pattern))
            )
        )
        .scalars()
        .all()
    )
    hits: list[SearchHit] = []
    for note in rows:
        score = _score(note.title, term) * 2 + _score(note.body, term)
        if score <= 0:
            continue
        hits.append(
            SearchHit(
                note_id=note.id,
                title=note.title,
                snippet=_snippet(note.body, term),
                score=score,
            )
        )
    hits.sort(key=lambda h: h.score, reverse=True)
    return hits[:limit]
