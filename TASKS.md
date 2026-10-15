# Combined Lab — Checklist

## Part A — make the security real (`app/main.py`)
- [ ] **TASK 1 (A04)** hash_password / verify_password use bcrypt
- [ ] **TASK 2 (A07)** create_token / read_token use a signed, expiring JWT
- [ ] **TASK 3 (A07)** get_current_user raises 401 on a bad/expired token or unknown user (fail closed)
- [ ] **TASK 4 (A01)** get_note returns 403 when the note isn't the caller's
- [ ] **TASK 5 (A01)** /admin/users requires the admin role and never returns the password column

## Part B — write the tests (`tests/`)
API (`test_api.py`)
- [ ] register then login returns a JWT (three dotted parts)
- [ ] wrong password returns 401
- [ ] create a note, then see it in your list

Security (`test_security.py`)
- [ ] bad token rejected (401)
- [ ] a user can't read another's note (403)  ← A01
- [ ] a user can read their own note (200)
- [ ] same login error for bad user vs bad password  ← A07
- [ ] a non-admin can't list users (403)  ← A01
- [ ] admin list has no password field  ← A04

**Goal:** all 5 tasks done AND all 11 tests green (`pytest -q`). Then `pytest --cov=app`.

## Reflection (4–5 sentences)
Pick one security test. Explain what it checks, which OWASP risk it guards, and what would break in the
app if a teammate deleted that one check.
