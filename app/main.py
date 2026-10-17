import os
import sqlite3
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError

app = FastAPI(title="SecureNotes API (Week 14 — starter)", version="1.0")

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
ALGORITHM = "HS256"
TOKEN_MINUTES = 30

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


# >>> TASK 1 — Hash passwords with bcrypt (A04 Cryptographic Failures)
def hash_password(raw: str) -> str:
    return pwd.hash(raw)

def verify_password(raw: str, hashed: str) -> bool:
    return pwd.verify(raw, hashed)
# <<< END TASK 1


# >>> TASK 2 — Issue & verify a JWT (A07 Authentication Failures)
def create_token(username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_MINUTES)
    to_encode = {"sub": username, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def read_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
# <<< END TASK 2


# --- database (in-memory SQLite, seeded on startup) -----------------------
db = sqlite3.connect(":memory:", check_same_thread=False)
db.row_factory = sqlite3.Row

def init_db():
    db.executescript(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            body TEXT NOT NULL
        );
        """
    )
    db.execute("INSERT INTO users (username,password,is_admin) VALUES (?,?,1)", ("admin", hash_password("admin123")))
    db.execute("INSERT INTO users (username,password,is_admin) VALUES (?,?,0)", ("alice", hash_password("alicepass")))
    db.execute("INSERT INTO users (username,password,is_admin) VALUES (?,?,0)", ("bob", hash_password("bobpass")))
    db.execute("INSERT INTO notes (owner_id,title,body) VALUES (2,'Alice diary','Alice secret note')")
    db.execute("INSERT INTO notes (owner_id,title,body) VALUES (3,'Bob plans','Bob secret note')")
    db.commit()

def reset_database():
    db.execute("DROP TABLE IF EXISTS users")
    db.execute("DROP TABLE IF EXISTS notes")
    init_db()

init_db()


class Credentials(BaseModel):
    username: str
    password: str

class NewNote(BaseModel):
    title: str
    body: str


# >>> TASK 3 — Validate the token and FAIL CLOSED
def get_current_user(token: str = Depends(oauth2)):
    username = read_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    row = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if not row:
        raise HTTPException(status_code=401, detail="User not found")
        
    return row
# <<< END TASK 3


def require_admin(user=Depends(get_current_user)):
    if not user["is_admin"]:
        raise HTTPException(status_code=403, detail="Admin required")
    return user


@app.post("/register")
def register(creds: Credentials):
    existing = db.execute("SELECT id FROM users WHERE username = ?", (creds.username,)).fetchone()
    if existing:
        raise HTTPException(status_code=409, detail="Username already taken")
    db.execute(
        "INSERT INTO users (username,password,is_admin) VALUES (?,?,0)",
        (creds.username, hash_password(creds.password)),
    )
    db.commit()
    return {"message": f"user {creds.username} created"}

@app.post("/login")
def login(creds: Credentials):
    row = db.execute(
        "SELECT id, username, password FROM users WHERE username = ?", (creds.username,)
    ).fetchone()
    if row is None or not verify_password(creds.password, row["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"access_token": create_token(row["username"]), "token_type": "bearer"}

@app.get("/notes")
def list_my_notes(user=Depends(get_current_user)):
    rows = db.execute("SELECT * FROM notes WHERE owner_id = ?", (user["id"],)).fetchall()
    return [dict(r) for r in rows]

@app.get("/notes/{note_id}")
def get_note(note_id: int, user=Depends(get_current_user)):
    row = db.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Note not found")
    # >>> TASK 4 — Ownership check (A01 Broken Access Control)
    if row["owner_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    # <<< END TASK 4
    return dict(row)

@app.post("/notes")
def create_note(note: NewNote, user=Depends(get_current_user)):
    cur = db.execute(
        "INSERT INTO notes (owner_id,title,body) VALUES (?,?,?)",
        (user["id"], note.title, note.body),
    )
    db.commit()
    return {"id": cur.lastrowid, "title": note.title}

@app.get("/admin/users")
def list_all_users(user=Depends(require_admin)):
    # >>> TASK 5 — Role check (A01 Broken Access Control)
    rows = db.execute("SELECT id, username, is_admin FROM users").fetchall()
    return [dict(r) for r in rows]
    # <<< END TASK 5

@app.get("/")
def home():
    return {"service": "SecureNotes API", "docs": "/docs"}