def test_root_redirects_to_ui(client):
    r = client.get("/", follow_redirects=False)
    assert r.status_code in (302, 307)
    assert r.headers["location"].rstrip("/") == "/ui"


def test_ui_index_served(client):
    r = client.get("/ui/")
    assert r.status_code == 200
    assert "<title>notebox</title>" in r.text
    assert "<script>" in r.text  # sanity: served the HTML, not JSON
