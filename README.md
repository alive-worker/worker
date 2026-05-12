# notebox

A small but real personal-notes HTTP API. Notes have a title, body (markdown),
and any number of tags. The service supports CRUD over notes and tags, simple
keyword search, and export to JSON / Markdown.

The project is intentionally compact (~700 lines of Python) but layered the
same way a real internal service would be: routers, schemas, models, services,
tests, seed script.

## Stack

- Python 3.11
- FastAPI + Uvicorn
- SQLAlchemy 2.x + SQLite
- Pydantic v2
- pytest

## Running locally

```bash
pip install -r requirements.txt
python -m scripts.seed              # creates notebox.db with sample data
uvicorn app.main:app --reload
```

OpenAPI docs at <http://127.0.0.1:8000/docs>.

## Running tests

```bash
pytest -q
```

## Layout

```
app/
  main.py            FastAPI entry
  db.py              engine / session
  models.py          SQLAlchemy models (Note, Tag, note_tag)
  schemas.py         Pydantic request / response schemas
  api/
    notes.py         /notes router
    tags.py          /tags router
    search.py        /search router
    export.py        /export router
  services/
    search.py        keyword search implementation
    export.py        JSON / Markdown export
scripts/
  seed.py            populate sample notes & tags
tests/
  test_notes.py
  test_tags.py
  test_search.py
```
