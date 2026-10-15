"""Security tests — the most valuable tests you'll write this week.

Each one locks in an OWASP rule from Weeks 13-14 so a future change can't quietly
reopen the hole. ONE example is done; replace each `assert False` TODO with a real test.

Seed data reminder:  note 1 belongs to ALICE, note 2 belongs to BOB.
Accounts:  admin/admin123 (admin) · alice/alicepass · bob/bobpass
"""
from tests.conftest import login, auth


# ----- EXAMPLE (already done) ---------------------------------------------
def test_protected_route_rejects_no_token(client):
    res = client.get("/notes")               # no Authorization header
    assert res.status_code == 401            # A07: auth is required


# ----- TODO 1 -------------------------------------------------------------
def test_protected_route_rejects_bad_token(client):
    # Call GET /notes with a junk token, e.g. auth("not.a.jwt").
    # Assert 401 — the app must fail closed on an invalid token.
    assert False, "TODO: write test_protected_route_rejects_bad_token"


# ----- TODO 2  (A01 — the big one) ----------------------------------------
def test_user_cannot_read_another_users_note(client):
    # Log in as alice. Try GET /notes/2 (that note belongs to Bob).
    # Assert 403 — ownership must be enforced.
    assert False, "TODO: write test_user_cannot_read_another_users_note"


# ----- TODO 3 -------------------------------------------------------------
def test_user_can_read_own_note(client):
    # Log in as alice. GET /notes/1 (hers). Assert 200.
    assert False, "TODO: write test_user_can_read_own_note"


# ----- TODO 4  (A07 — no user enumeration) --------------------------------
def test_login_does_not_reveal_which_field_was_wrong(client):
    # POST /login once with a username that doesn't exist, once with a real
    # username but wrong password. Assert the two error bodies are IDENTICAL.
    assert False, "TODO: write test_login_does_not_reveal_which_field_was_wrong"


# ----- TODO 5  (A01 — role) -----------------------------------------------
def test_non_admin_cannot_list_users(client):
    # Log in as alice (not an admin). GET /admin/users. Assert 403.
    assert False, "TODO: write test_non_admin_cannot_list_users"


# ----- TODO 6  (A04 — no hash leak) ---------------------------------------
def test_admin_can_list_users_without_password_leak(client):
    # Log in as admin. GET /admin/users. Assert 200 AND no item in the
    # response contains a "password" field.
    assert False, "TODO: write test_admin_can_list_users_without_password_leak"
