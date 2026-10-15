"""Security tests — the most valuable tests you'll write this week."""
from tests.conftest import login, auth


# ----- EXAMPLE (already done) ---------------------------------------------
def test_protected_route_rejects_no_token(client):
    res = client.get("/notes")               # no Authorization header
    assert res.status_code == 401            # A07: auth is required


# ----- TODO 1 -------------------------------------------------------------
def test_protected_route_rejects_bad_token(client):
    res = client.get("/notes", headers=auth("not.a.jwt"))
    assert res.status_code == 401


# ----- TODO 2  (A01 — the big one) ----------------------------------------
def test_user_cannot_read_another_users_note(client):
    alice_token = login(client, "alice", "alicepass")
    res = client.get("/notes/2", headers=auth(alice_token))  # Note 2 belongs to Bob
    assert res.status_code == 403


# ----- TODO 3 -------------------------------------------------------------
def test_user_can_read_own_note(client):
    alice_token = login(client, "alice", "alicepass")
    res = client.get("/notes/1", headers=auth(alice_token))  # Note 1 belongs to Alice
    assert res.status_code == 200


# ----- TODO 4  (A07 — no user enumeration) --------------------------------
def test_login_does_not_reveal_which_field_was_wrong(client):
    res_fake_user = client.post("/login", json={"username": "nonexistent", "password": "wrongpassword"})
    res_wrong_pass = client.post("/login", json={"username": "alice", "password": "wrongpassword"})
    
    assert res_fake_user.status_code == 401
    assert res_wrong_pass.status_code == 401
    assert res_fake_user.json() == res_wrong_pass.json()


# ----- TODO 5  (A01 — role) -----------------------------------------------
def test_non_admin_cannot_list_users(client):
    alice_token = login(client, "alice", "alicepass")
    res = client.get("/admin/users", headers=auth(alice_token))
    assert res.status_code == 403


# ----- TODO 6  (A04 — no hash leak) ---------------------------------------
def test_admin_can_list_users_without_password_leak(client):
    admin_token = login(client, "admin", "admin123")
    res = client.get("/admin/users", headers=auth(admin_token))
    assert res.status_code == 200
    
    users = res.json()
    assert len(users) > 0
    for u in users:
        assert "password" not in u