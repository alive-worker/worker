from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import get_session
from app.schemas import SearchHit
from app.services.search import keyword_search

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=list[SearchHit])
def search(q: str = Query(min_length=1), limit: int = 20, db: Session = Depends(get_session)):
    return keyword_search(db, q, limit=limit)
