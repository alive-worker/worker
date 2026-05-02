from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


note_tag = Table(
    "note_tag",
    Base.metadata,
    Column("note_id", ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=_utcnow, onupdate=_utcnow, nullable=False
    )

    tags: Mapped[list["Tag"]] = relationship(
        "Tag", secondary=note_tag, back_populates="notes", lazy="selectin"
    )


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    notes: Mapped[list[Note]] = relationship(
        "Note", secondary=note_tag, back_populates="tags"
    )
