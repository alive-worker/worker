def _make(client, title, body, tags=None):
    return client.post(
        "/notes",
        json={"title": title, "body": body, "tags": tags or []},
    ).json()


def test_search_matches_title_and_body(client):
    _make(client, "FastAPI tips", "use Depends for sessions")
    _make(client, "SQLite tricks", "PRAGMA journal_mode=WAL")
    _make(client, "Unrelated", "nothing to see")

    hits = client.get("/search", params={"q": "fastapi"}).json()
    assert len(hits) == 1
    assert hits[0]["title"] == "FastAPI tips"


def test_search_ranks_title_above_body(client):
    a = _make(client, "alpha topic", "mentions beta once")
    b = _make(client, "another", "beta beta beta beta")
    hits = client.get("/search", params={"q": "beta"}).json()
    assert [h["note_id"] for h in hits][0] == b["id"]
    assert a["id"] in [h["note_id"] for h in hits]


def test_search_respects_limit(client):
    for i in range(5):
        _make(client, f"note {i}", "common-word here")
    hits = client.get("/search", params={"q": "common-word", "limit": 2}).json()
    assert len(hits) == 2
