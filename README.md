# SecureNotes API — Combined Lab (Student Starter)

One lab, two halves:
- **Part A** — make the app's security real (JWT auth + authorization).
- **Part B** — write the tests that prove Part A works and won't silently break.

## Setup
```bash
python -m venv venv
# Windows:  venv\Scripts\activate   ·   macOS/Linux:  source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload     # the app (fake security for now)
pytest -q                         # the tests: 2 pass, the rest are TODO (red)
```
Open http://127.0.0.1:8000/docs. Accounts: `admin/admin123`, `alice/alicepass` (note 1), `bob/bobpass` (note 2).

> **Keep the bcrypt pin.** `requirements.txt` pins `bcrypt==4.0.1` — newer bcrypt breaks passlib.

## What you edit
- **Part A:** `app/main.py`, only inside the `>>> TASK n ... <<< END TASK n` markers.
- **Part B:** `tests/test_api.py` and `tests/test_security.py` — replace each `assert False, "TODO..."`.
  (`tests/conftest.py` gives you the `client` fixture and `login` / `auth` helpers — don't edit it.)

**The payoff:** the tests you write in Part B are the proof your Part A works. When your auth is
correct, your tests go green. See the handout and `TASKS.md`.

## Part D — peer review on GitHub
Push to a public repo, commit the starter first, then your work on a `secure-and-test` branch, and open
a pull request for a partner pair to review. See the handout (Part D).
