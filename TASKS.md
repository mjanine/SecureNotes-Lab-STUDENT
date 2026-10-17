# Combined Lab — Checklist

## Part A — make the security real (`app/main.py`)

* [x] **TASK 1 (A04)** hash_password / verify_password use bcrypt
* [x] **TASK 2 (A07)** create_token / read_token use a signed, expiring JWT
* [x] **TASK 3 (A07)** get_current_user raises 401 on a bad/expired token or unknown user (fail closed)
* [x] **TASK 4 (A01)** get_note returns 403 when the note isn't the caller's
* [x] **TASK 5 (A01)** /admin/users requires the admin role and never returns the password column

## Part B — write the tests (`tests/`)

API (`test_api.py`)

* [x] register then login returns a JWT (three dotted parts)
* [x] wrong password returns 401
* [x] create a note, then see it in your list

Security (`test_security.py`)

* [x] bad token rejected (401)
* [x] a user can't read another's note (403)  ← A01
* [x] a user can read their own note (200)
* [x] same login error for bad user vs bad password  ← A07
* [x] a non-admin can't list users (403)  ← A01
* [x] admin list has no password field  ← A04

**Goal:** all 5 tasks done AND all 11 tests green (`pytest -q`). Then `pytest --cov=app`.

## Reflection

The `test_user_cannot_read_another_users_note` test verifies that an authenticated user receives an `HTTP 403 Forbidden` response when attempting to access a note owned by another account. This locks in the **OWASP A01: Broken Access Control** vulnerability, specifically preventing Insecure Direct Object Reference (IDOR) attacks where resource IDs in URL parameters are manipulated. If a teammate removed the ownership check `if row["owner_id"] != user["id"]` in `app/main.py`, any valid user could read all confidential notes stored in the system simply by changing the ID in the endpoint path. Having this automated test in place ensures that broken authorization logic will immediately fail the build before reaching production.