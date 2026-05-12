from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Note


def _note_to_dict(note: Note) -> dict:
    return {
        "id": note.id,
        "title": note.title,
        "body": note.body,
        "created_at": note.created_at.isoformat(),
        "updated_at": note.updated_at.isoformat(),
        "tags": [t.name for t in note.tags],
    }


def _note_to_markdown(note: Note) -> str:
    tag_line = ""
    if note.tags:
        tag_line = "\n*tags: " + ", ".join(f"`{t.name}`" for t in note.tags) + "*\n"
    return f"# {note.title}\n{tag_line}\n{note.body}\n"


def export_notes(db: Session, *, fmt: str) -> list[dict] | str:
    notes = db.execute(select(Note).order_by(Note.created_at)).scalars().all()
    if fmt == "json":
        return [_note_to_dict(n) for n in notes]
    return "\n\n---\n\n".join(_note_to_markdown(n) for n in notes)
