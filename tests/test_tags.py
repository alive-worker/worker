def test_create_tag(client):
    r = client.post("/tags", json={"name": "python"})
    assert r.status_code == 201
    assert r.json()["name"] == "python"


def test_create_duplicate_tag_conflicts(client):
    client.post("/tags", json={"name": "python"})
    r = client.post("/tags", json={"name": "python"})
    assert r.status_code == 409


def test_list_tags_sorted(client):
    for name in ["zeta", "alpha", "mu"]:
        client.post("/tags", json={"name": name})
    names = [t["name"] for t in client.get("/tags").json()]
    assert names == sorted(names)

# NOTE: deliberately missing coverage for tag deletion behaviour; one of the
# prompts asks the agent to extend this file.
