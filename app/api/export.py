from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from sqlalchemy.orm import Session

from app.db import get_session
from app.services.export import export_notes

router = APIRouter(prefix="/export", tags=["export"])


@router.get("")
def export(format: str = "json", db: Session = Depends(get_session)):
    if format not in {"json", "markdown"}:
        raise HTTPException(status_code=400, detail="format must be json or markdown")
    payload = export_notes(db, fmt=format)
    if format == "json":
        return JSONResponse(content=payload)
    return PlainTextResponse(content=payload, media_type="text/markdown")
