# FastAPI JWT Authentication — Reference Guide

A personal reference for implementing secure username/password authentication with role-based access control in FastAPI. Built with PostgreSQL, PyJWT, and pwdlib.

---

## 1. What This System Does

A user can:
1. **Sign up** — creates an account, password is hashed before storage
2. **Log in** — verifies credentials, returns a signed JWT
3. **Access protected routes** — sends the JWT on every request, server verifies it
4. **Access role-restricted routes** — server checks the user's role (from inside the token) before allowing access

```
Signup ──▶ stored in DB (hashed password)
Login  ──▶ verify password ──▶ issue JWT (contains username + role)
Protected route ──▶ read JWT from header ──▶ verify signature ──▶ allow/deny
Role-restricted route ──▶ same as above + check role claim
```

---

## 2. Project Structure

```
auth/
├── __init__.py          # marks this folder as a Python package
├── main.py              # FastAPI app, routes, JWT creation, dependencies
├── models.py             # SQLAlchemy table definitions
├── schemas.py             # Pydantic request/response shapes
├── utils.py                # password hashing helpers
├── auth_database.py         # DB connection + session setup
.env                          # secrets (never commit this)
```

> Note: whether you run this as `auth.main:app` (from the parent folder, using relative imports `from . import`) or `main:app` (from inside `auth/`, using flat imports `import`) depends on where you launch uvicorn from. Pick one and stay consistent — mixing the two causes `ModuleNotFoundError`.

---

## 3. `.env` — Secrets

```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=a_long_random_string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Generate a good secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Never** commit `.env` — add it to `.gitignore`.

---

## 8. `main.py` — App, Routes, Auth Logic

### Imports explained

```python
from fastapi import FastAPI, Depends, HTTPException, status
```
| Import | Purpose |
|---|---|
| `FastAPI` | The core app object everything attaches to |
| `Depends` | Declares a dependency — "run this first, inject the result" |
| `HTTPException` | Used to return proper HTTP errors (401, 403, 400, etc.) |
| `status` | Named HTTP status codes (`status.HTTP_401_UNAUTHORIZED`) instead of magic numbers |

```python
from sqlalchemy.orm import Session
```
| Import | Purpose |
|---|---|
| `Session` | Type hint for a database session object |

```python
import models, schemas, utils
from auth_database import get_db, Base, engine
```
Your own modules: table definitions, request/response shapes, password helpers, and the DB session/engine.

```python
import os
from dotenv import load_dotenv
```
| Import | Purpose |
|---|---|
| `load_dotenv` | Reads `.env` and loads its values into the environment |
| `os` | Used to actually read those values (`os.getenv(...)`) |

```python
import jwt
from jwt import PyJWTError
```
| Import | Purpose |
|---|---|
| `jwt` (pyjwt) | Encodes (creates) and decodes (verifies) JWT tokens |
| `PyJWTError` | Base exception raised for any invalid/expired/malformed token |

```python
from datetime import datetime, timedelta, timezone
```
Used to calculate token expiration timestamps, always in UTC.

```python
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
```
| Import | Purpose |
|---|---|
| `OAuth2PasswordRequestForm` | Parses `username`/`password` from a login form submission |
| `OAuth2PasswordBearer` | Extracts the token from the `Authorization: Bearer <token>` header on protected routes |

### Setup

```python
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

Base.metadata.create_all(bind=engine)   # creates tables in Postgres if they don't exist yet

app = FastAPI()
```

### `create_access_token(data: dict)`

**Job:** package a dictionary of claims into a signed, expiring JWT string.

```python
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

| Line | What it does |
|---|---|
| `data.copy()` | Avoids mutating the caller's original dict |
| `expire = ...` | Calculates "now + N minutes" as the expiration time |
| `to_encode.update({'exp': expire})` | `exp` is a reserved JWT claim name — `pyjwt` automatically enforces it on decode |
| `jwt.encode(...)` | Produces the signed token string, using `SECRET_KEY` to generate the signature |

Doesn't touch the database — pure function, just packages data into a token.

### `POST /signup`

```python
@app.post('/signup')
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
```

| Step | What happens |
|---|---|
| 1 | Check if the username already exists — reject with `400` if so |
| 2 | Hash the incoming plain password |
| 3 | Build a new `User` model instance |
| 4 | `db.add()` — stage the insert; `db.commit()` — actually run it; `db.refresh()` — reload the object so it has its real DB-generated `id` |
| 5 | Return the new user's public info, **excluding** the password |

### `POST /login`

```python
@app.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
```

| Step | What happens |
|---|---|
| 1 | Look up the user by `form_data.username` |
| 2 | If no user found → `401 Invalid Username` |
| 3 | If password doesn't match → `401 Invalid Password` |
| 4 | Build `token_data` with `sub` (subject/username) and `role` |
| 5 | Create and return the JWT as `access_token` |

> `sub` is a standard JWT claim name meaning "who this token is about." Including `role` here means role checks don't require a second database lookup later.

### `get_current_user(token)` — the core verification dependency

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credential",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credential_exception
    except PyJWTError:
        raise credential_exception

    return {"username": username, "role": role}
```

| Step | What happens |
|---|---|
| `Depends(oauth2_scheme)` | Extracts the token string from the `Authorization` header automatically |
| `jwt.decode(...)` | Verifies the signature and expiration; raises `PyJWTError` if invalid/expired |
| `algorithms=[ALGORITHM]` | Must be a **list**, even with a single algorithm |
| checks for `None` | Guards against a token that's technically valid but missing expected claims |
| returns a dict | This becomes `current_user` in any route that depends on this function |

### `required_roles(allowed_roles)` — a dependency factory

```python
def required_roles(allowed_roles: list[str]):
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user.get("role") not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permission")
        return current_user
    return role_checker
```

This is a **function that returns a dependency**, letting you parameterize which roles are allowed per-route:

```python
@app.get("/user/dashboard")
def user_dashboard(current_user: dict = Depends(required_roles(["user"]))):
    ...
```

`required_roles(["user"])` runs immediately when the route is defined, building a custom `role_checker` closure that remembers `["user"]`. `Depends()` then uses *that* returned function as the actual dependency.

**Why 403, not 401 here:** `get_current_user` already confirmed the token is valid (401 territory — "who even are you"). `required_roles` is a separate check for "I know who you are, you're just not allowed" — that's what 403 means.

---

## 9. Full Request Flow (End to End)

```
1. POST /signup
   Body: {username, email, password, role}
   → password hashed → user row created → returns public user info

2. POST /login
   Body (form): username=...&password=...
   → OAuth2PasswordRequestForm parses it
   → credentials checked against DB
   → JWT created with {sub, role, exp}
   ← {access_token, token_type: "bearer"}

3. GET /protected  (or any protected route)
   Header: Authorization: Bearer <token>
   → OAuth2PasswordBearer extracts the token
   → get_current_user decodes + verifies it
   → route runs with current_user available

4. GET /user/dashboard  (role-restricted)
   Same as step 3, plus:
   → required_roles(["user"]) checks current_user["role"]
   → 403 if role doesn't match, otherwise proceeds
```

---

## 10. Quick Reference — Imports by Purpose

| Need | Import | Package |
|---|---|---|
| App, routing, DI, errors | `FastAPI, Depends, HTTPException, status` | `fastapi` |
| Login form parsing | `OAuth2PasswordRequestForm` | `fastapi.security` |
| Token extraction from header | `OAuth2PasswordBearer` | `fastapi.security` |
| DB session type | `Session` | `sqlalchemy.orm` |
| DB engine/tables | `create_engine, Column, Integer, String` | `sqlalchemy` |
| Base class for models | `declarative_base` | `sqlalchemy.orm` |
| Session factory | `sessionmaker` | `sqlalchemy.orm` |
| Request/response validation | `BaseModel` | `pydantic` |
| Password hashing | `PasswordHash` | `pwdlib` |
| JWT create/verify | `jwt`, `PyJWTError` (or `InvalidTokenError`) | `pyjwt` |
| Env variables | `load_dotenv` | `dotenv` |
| Expiration math | `datetime, timedelta, timezone` | (built-in) |
| No import, but required | — | `python-multipart` (form parsing), `uvicorn` (server), `psycopg2-binary` (Postgres driver) |

**Install command:**
```bash
python -m pip install fastapi uvicorn sqlalchemy psycopg2-binary pyjwt "pwdlib[argon2]" python-multipart python-dotenv
```

---

## 11. Common Pitfalls (learned the hard way)

- `jwt.decode(..., algorithms=ALGORITHM)` — must be a **list**: `algorithms=[ALGORITHM]`
- Mixing relative (`from .`) and flat (`import`) imports depending on how you launch uvicorn — pick one style and match your run command to it
- `python-multipart` has no explicit import but is required for `OAuth2PasswordRequestForm` to work
- Duplicate function names across routes (e.g. two functions both named the same) — FastAPI won't complain, but Python will silently let the second overwrite the first in the namespace
- On Windows/Git Bash, bare `pip`/`uvicorn` can resolve to the wrong Python if multiple installs exist — use `python -m pip` / `python -m uvicorn` if `which <tool>` doesn't point inside your venv
- 401 vs 403 — use 401 when identity can't be verified at all, 403 when identity is known but not permitted

---

