"""API behaviour tests.

ONE example is written for you. Replace each `assert False` TODO with a real test.
Use the helpers from conftest:   login(client, user, pw) -> token,   auth(token) -> header.
Ask for the `client` fixture by adding it as a parameter (it gives you a fresh DB each time).

Run the suite:   pytest -q
Run one file:    pytest tests/test_api.py -q
"""
from tests.conftest import login, auth


# ----- EXAMPLE (already done) ---------------------------------------------
def test_home_ok(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["service"] == "SecureNotes API"


# ----- TODO 1 -------------------------------------------------------------
def test_register_then_login(client):
    # 1. Register a new user
    reg_res = client.post("/register", json={"username": "charlie", "password": "charliepass"})
    assert reg_res.status_code == 200

    # 2. Log in as that user
    login_res = client.post("/login", json={"username": "charlie", "password": "charliepass"})
    assert login_res.status_code == 200

    # 3. Assert access_token looks like a JWT (three dot-separated parts)
    token = login_res.json().get("access_token")
    assert token is not None
    assert token.count(".") == 2


# ----- TODO 2 -------------------------------------------------------------
def test_login_wrong_password_is_401(client):
    res = client.post("/login", json={"username": "alice", "password": "wrongpassword"})
    assert res.status_code == 401


# ----- TODO 3 -------------------------------------------------------------
def test_create_then_list_own_note(client):
    # Log in as alice using the helper to get her token & auth headers
    token = login(client, "alice", "alicepass")
    headers = auth(token)

    # POST a new note
    note_payload = {"title": "Alice Special Note", "body": "Top secret content"}
    create_res = client.post("/notes", json=note_payload, headers=headers)
    assert create_res.status_code == 200

    # GET /notes and verify the title appears in the list
    list_res = client.get("/notes", headers=headers)
    assert list_res.status_code == 200
    
    titles = [note["title"] for note in list_res.json()]
    assert "Alice Special Note" in titles