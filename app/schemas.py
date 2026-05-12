from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class TagOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class TagCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)


class NoteBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    body: str = ""


class NoteCreate(NoteBase):
    tags: list[str] = Field(default_factory=list)


class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    body: str | None = None
    tags: list[str] | None = None


class NoteOut(NoteBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime
    tags: list[TagOut]


class SearchHit(BaseModel):
    note_id: int
    title: str
    snippet: str
    score: float


class ExportFormat(BaseModel):
    format: str = Field(pattern="^(json|markdown)$")
