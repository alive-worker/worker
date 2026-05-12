from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import Tag
from app.schemas import TagCreate, TagOut

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("", response_model=list[TagOut])
def list_tags(db: Session = Depends(get_session)):
    return db.execute(select(Tag).order_by(Tag.name)).scalars().all()


@router.post("", response_model=TagOut, status_code=status.HTTP_201_CREATED)
def create_tag(payload: TagCreate, db: Session = Depends(get_session)):
    name = payload.name.strip().lower()
    existing = db.execute(select(Tag).where(Tag.name == name)).scalar_one_or_none()
    if existing is not None:
        raise HTTPException(status_code=409, detail="tag already exists")
    tag = Tag(name=name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(tag_id: int, db: Session = Depends(get_session)):
    tag = db.get(Tag, tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="tag not found")
    # BUG-FOR-PROMPT: the secondary note_tag rows should be cleared first.
    # Without ON DELETE CASCADE being honored by SQLite at the engine level,
    # deleting a tag that is still attached to notes leaves orphan rows in
    # note_tag. This is the bug targeted by the "tag delete leaves dangling
    # associations" task.
    db.delete(tag)
    db.commit()
