def test_create_and_get_note(client):
    r = client.post("/notes", json={"title": "hello", "body": "world", "tags": ["a", "B"]})
    assert r.status_code == 201
    note = r.json()
    assert note["title"] == "hello"
    assert {t["name"] for t in note["tags"]} == {"a", "b"}

    r2 = client.get(f"/notes/{note['id']}")
    assert r2.status_code == 200
    assert r2.json()["id"] == note["id"]


def test_list_notes_returns_all(client):
    for i in range(3):
        client.post("/notes", json={"title": f"t{i}", "body": "", "tags": []})
    r = client.get("/notes")
    assert r.status_code == 200
    assert len(r.json()) == 3


def test_patch_note_updates_fields_and_tags(client):
    created = client.post("/notes", json={"title": "old", "body": "x", "tags": ["one"]}).json()
    r = client.patch(
        f"/notes/{created['id']}",
        json={"title": "new", "tags": ["one", "two"]},
    )
    assert r.status_code == 200
    note = r.json()
    assert note["title"] == "new"
    assert note["body"] == "x"
    assert {t["name"] for t in note["tags"]} == {"one", "two"}


def test_delete_note(client):
    created = client.post("/notes", json={"title": "gone", "body": "", "tags": []}).json()
    r = client.delete(f"/notes/{created['id']}")
    assert r.status_code == 204
    assert client.get(f"/notes/{created['id']}").status_code == 404


def test_get_missing_note_returns_404(client):
    assert client.get("/notes/9999").status_code == 404
