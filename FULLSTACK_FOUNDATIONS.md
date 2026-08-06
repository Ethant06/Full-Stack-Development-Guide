# Full-Stack Foundations Guide

A practical guide for building apps like this Workout project over and over again.

This document covers:

- How frontend and backend fit together
- Next.js (App Router) folder structure
- `.js` vs `.jsx` vs `.ts` vs `.tsx`
- Pages, layouts, routing, and navigation
- Auth, API clients, and connecting to FastAPI
- Backend basics (`load_dotenv`, routers, CORS, JWTs)
- Habits and best practices you’ll reuse on every project

Your current project shape:

```text
Workout/
├── backend/                 # FastAPI + SQLAlchemy + PostgreSQL
│   ├── .env                 # Secrets (not committed)
│   ├── .venv/               # Python virtual environment
│   ├── requirements.txt
│   └── app/
│       ├── main.py          # FastAPI app entrypoint
│       ├── database.py      # DB engine + sessions
│       ├── models.py        # SQLAlchemy tables
│       ├── schemas.py       # Pydantic request/response shapes
│       ├── deps.py          # Shared dependencies (auth)
│       └── routers/         # Route modules (auth, workouts, routines)
└── frontend/                # Next.js + React
    ├── app/                 # Routes (App Router)
    ├── components/          # Reusable UI
    ├── context/             # React Context (auth state)
    └── lib/                 # Helpers (axios api client)
```

---

## 1. The Big Picture: What Each Side Does

Think of a full-stack app as two programs that talk over HTTP.

### Backend (FastAPI) — the brain / data layer

Responsible for:

- Business rules (“is this password correct?”)
- Talking to the database
- Auth (signup, login, JWT validation)
- Exposing stable APIs like:
  - `POST /auth/signup`
  - `POST /auth/login`
  - `GET /workouts/workouts`

The backend does **not** render your React pages. It returns JSON.

### Frontend (Next.js / React) — the face / interaction layer

Responsible for:

- Showing UI
- Collecting user input (forms, buttons)
- Calling the backend with `fetch` / `axios`
- Keeping client state (logged-in user, loading flags)
- Routing between pages (`/`, `/login`)

### The contract between them

Frontend and backend stay compatible when they agree on:

1. **URL** — e.g. `http://localhost:8000/auth/login`
2. **HTTP method** — `GET`, `POST`, `DELETE`, etc.
3. **Request body / query shape**
4. **Response shape** — e.g. `{ "access_token": "...", "token_type": "bearer" }`
5. **Auth header** — e.g. `Authorization: Bearer <token>`
6. **CORS** — browser security allowing `localhost:3000` → `localhost:8000`

If any of those disagree, things break even if each side “looks fine” alone.

---

## 2. How a Typical Request Flows

Example: logging in.

```text
Browser (localhost:3000)
  │
  │ 1. User submits login form
  │ 2. AuthContext.login() runs
  │ 3. axios POST /auth/login with username+password
  ▼
api.js (baseURL http://localhost:8000)
  │
  │ 4. Browser sends HTTP request
  ▼
FastAPI (localhost:8000)
  │
  │ 5. auth router checks DB password
  │ 6. Creates JWT
  │ 7. Returns { access_token, token_type }
  ▼
AuthContext
  │
  │ 8. Saves token in localStorage
  │ 9. setUser(...)
  │ 10. router.push("/")
  ▼
Home page (/) renders for logged-in user
```

Later protected API calls (like fetching workouts) automatically attach:

```http
Authorization: Bearer <token>
```

Your `lib/api.js` interceptor does that.

---

## 3. Frontend Folder Structure (Professional Pattern)

Solid, common Next.js App Router structure:

```text
frontend/
├── app/                         # Routing lives here (special Next.js folder)
│   ├── layout.js|tsx            # Shared shell (html/body, nav, providers)
│   ├── page.js|tsx              # Route: "/"  (home)
│   ├── globals.css
│   ├── login/
│   │   └── page.js|tsx          # Route: "/login"
│   ├── workouts/
│   │   ├── page.tsx             # Route: "/workouts"
│   │   └── [id]/
│   │       └── page.tsx         # Route: "/workouts/123"
│   └── api/                     # (optional) Next.js Route Handlers
│       └── ...
├── components/                  # Reusable UI pieces (NavBar, forms, cards)
│   ├── NavBar.js
│   └── ProtectedRoute.js
├── context/                     # Global client state (AuthContext)
│   └── AuthContext.js
├── lib/                         # Non-UI utilities
│   └── api.js                   # axios instance + interceptors
├── hooks/                       # (optional) custom hooks: useAuth, useWorkouts
├── types/                       # (optional) shared TypeScript types
├── public/                      # Static assets (images, favicon)
├── package.json
└── next.config.ts
```

### What goes where (rules of thumb)

| Folder | Put here | Don’t put here |
|---|---|---|
| `app/` | Pages/layouts that map to URLs | Random helpers |
| `components/` | Reusable visual building blocks | Page-specific route files |
| `context/` | Cross-page shared state | One-off local form state |
| `lib/` | API clients, formatters, constants | React components |
| `hooks/` | Reusable stateful logic | UI markup |
| `types/` | Shared TS interfaces | Runtime logic |

### Your Workout frontend mapped to that idea

- `app/page.tsx` → home (`/`)
- `app/login/page.js` → login (`/login`)
- `app/layout.js` → wraps every page with `AuthProvider` + `NavBar`
- `components/ProtectedRoute.js` → gate for logged-in-only content
- `context/AuthContext.js` → login/signup/logout + user state
- `lib/api.js` → single axios client pointed at FastAPI

---

## 4. `.js` vs `.jsx` vs `.ts` vs `.tsx` (Why Mixing Exists)

### Plain English

| Extension | Language | Can contain JSX (`<div>`) | Type checking |
|---|---|---|---|
| `.js` | JavaScript | Technically yes in Next.js, but `.jsx` is clearer | No |
| `.jsx` | JavaScript + JSX | Yes | No |
| `.ts` | TypeScript | No | Yes |
| `.tsx` | TypeScript + JSX | Yes | Yes |

JSX means writing HTML-like tags inside JavaScript/TypeScript:

```tsx
return <h1>Hello</h1>;
```

### Why your project has both `.js` and `.tsx`

Next.js allows JavaScript and TypeScript side by side.

In this repo:

- Many files started as `.js` (faster to write while learning)
- `page.tsx` uses TypeScript because typed `Workout` objects catch bugs early
  (`id`, `name`, `description` errors)

### What should you do going forward?

Pick a default and stay consistent.

**Good beginner-friendly path:**

1. Learn with `.js` / `.jsx` first
2. Move page-by-page to `.tsx` as you want safer props/data

**Professional default for new apps:**

- Prefer TypeScript everywhere:
  - pages/components: `.tsx`
  - utilities/types: `.ts`

### Important rule

Do **not** put both `page.js` and `page.tsx` in the same folder. Next.js will conflict. One route file only.

---

## 5. Next.js App Router: Pages, Default Route, Switching Pages

Next.js uses the filesystem for routing. Folder names under `app/` become URL segments.

### Default page (`/`)

File:

```text
app/page.tsx
```

URL:

```text
http://localhost:3000/
```

That is the homepage. No extra router config needed.

### Nested page (`/login`)

File:

```text
app/login/page.js
```

URL:

```text
http://localhost:3000/login
```

### Dynamic page example

File:

```text
app/workouts/[id]/page.tsx
```

URL examples:

```text
/workouts/1
/workouts/42
```

In the page:

```tsx
export default async function WorkoutPage({ params }) {
  const { id } = await params;
  // fetch workout by id
}
```

(Exact `params` style can vary by Next.js version; always check current docs for your version.)

### `layout.js` / `layout.tsx`

Layouts wrap child pages and persist across navigations.

Your root layout:

```js
// app/layout.js
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <NavBar />
          {children}   {/* <-- the current page gets injected here */}
        </AuthProvider>
      </body>
    </html>
  );
}
```

So:

- Visiting `/` → layout + `app/page.tsx`
- Visiting `/login` → same layout + `app/login/page.js`

That’s why `NavBar` appears on every page.

### Switching pages (client-side navigation)

#### Option A: `<Link>` (preferred for normal navigation)

```jsx
import Link from "next/link";

<Link href="/login">Login</Link>
<Link href="/">Home</Link>
```

Benefits:

- Prefetching
- Faster client transitions
- No full browser reload

#### Option B: `useRouter()` (programmatic redirects)

Used after login/logout:

```js
import { useRouter } from "next/navigation";

const router = useRouter();
router.push("/");        // go home
router.push("/login");   // go login
router.replace("/login"); // redirect without keeping history entry
```

Your `AuthContext` does this after login/logout.

### Protected pages

Not every page should be public.

Pattern used here:

1. `ProtectedRoute` checks `user` from context
2. If no user → redirect to `/login`
3. If user exists → render children

```jsx
<ProtectedRoute>
  <HomeContent />
</ProtectedRoute>
```

---

## 6. `"use client"` vs Server Components (Critical Mental Model)

Next.js App Router components are **Server Components by default**.

### Server Components

- Run on the server
- Great for static markup, SEO, secure data fetching
- Cannot use browser-only APIs:
  - `useState`, `useEffect`
  - `localStorage`
  - click handlers in many cases
  - browser-only libraries blindly

### Client Components

Add this at the top of the file:

```js
"use client";
```

Needed when you use:

- React state/hooks
- Event handlers (`onClick`, `onSubmit`)
- Context (`useContext`)
- `localStorage`
- Client routing hooks (`useRouter` for redirects after actions)

In your app, these are client components:

- `AuthContext.js`
- `login/page.js`
- `ProtectedRoute.js`
- `NavBar.js`
- home page content in `page.tsx`

### Practical rule

- Start files as Server Components
- Switch to `"use client"` only when interactivity/browser APIs force it
- Keep providers (like Auth) high in the tree via `layout.js`

---

## 7. React State Patterns You’ll Reuse Forever

### Local state (`useState`)

For one component:

```js
const [username, setUsername] = useState("");
```

Use for form fields, toggles, temporary UI flags.

### Shared state (Context)

For many components needing the same data (auth user):

```js
const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  return (
    <AuthContext.Provider value={{ user, setUser, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
```

Then any child can do:

```js
const { user, login, logout } = useContext(AuthContext);
```

### Persistence (`localStorage`)

Browser storage survives refresh.

Typical auth pattern:

1. Login success → save token
2. On app load → read token back into state
3. Logout → remove token

```js
localStorage.setItem("token", token);
localStorage.getItem("token");
localStorage.removeItem("token");
```

Remember: `localStorage` only exists in the browser (`window`). Guard it in Next.js when needed:

```js
if (typeof window !== "undefined") {
  // safe to use localStorage
}
```

---

## 8. Connecting Frontend ↔ Backend (The Reusable Setup)

### Step 1: Create one API client

File: `frontend/lib/api.js`

```js
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

export default api;
```

Why this is professional:

- One place for base URL
- One place for auth headers
- Pages stay clean: `api.get("/workouts/workouts")`

### Step 2: Match backend routes exactly

Backend:

```py
@router.post("/login")  # with prefix="/auth" → /auth/login
```

Frontend:

```js
await api.post("/auth/login", formData, {
  headers: { "Content-Type": "application/x-www-form-urlencoded" },
});
```

### Step 3: Know content types

| Use case | Content-Type | Body helper |
|---|---|---|
| Normal JSON APIs | `application/json` | `api.post(url, { username, password })` |
| OAuth2 password form (FastAPI) | `application/x-www-form-urlencoded` | `URLSearchParams` |
| File uploads | `multipart/form-data` | `FormData` |

Your login endpoint uses FastAPI’s `OAuth2PasswordRequestForm`, so form-urlencoded is required. We recommend using JSON for login

Signup can be JSON because it uses a Pydantic model:

```js
await api.post("/auth/signup", { username, password });
```

### Step 4: Enable CORS on backend

Browsers block cross-origin calls unless backend allows them.

Your FastAPI CORS:

```py
allow_origins=["http://localhost:3000"]
```

Frontend runs on `:3000`, backend on `:8000` → different origins → CORS required.

### Step 5: Use env vars for URLs (better than hardcoding)

Instead of hardcoding forever:

```js
baseURL: process.env.NEXT_PUBLIC_API_URL
```

In `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Notes:

- In Next.js, browser-visible env vars must start with `NEXT_PUBLIC_`
- Restart `npm run dev` after changing env files

---

## 9. Backend Foundations You’ll Reuse

### App entrypoint (`main.py`)

Typical responsibilities:

1. Create FastAPI app
2. Configure CORS
3. Create DB tables (dev convenience) or run migrations
4. Include routers

```py
app = FastAPI()
app.add_middleware(CORSMiddleware, ...)
app.include_router(auth.router)
app.include_router(workouts.router)
```

### Routers

Split by feature:

```text
routers/
├── auth.py
├── workouts.py
└── routines.py
```

Each router has a prefix/tag:

```py
router = APIRouter(prefix="/auth", tags=["auth"])
```

### Models vs Schemas

- `models.py` → database tables (SQLAlchemy)
- `schemas.py` → API request/response validation (Pydantic)

This separation keeps DB structure and API contract cleaner.

### Dependencies (`deps.py`)

Reusable “ingredients” injected into endpoints:

```py
def get_current_user(token: str = Depends(oauth2_bearer)):
    ...
    return {"username": ..., "id": ...}
```

Then:

```py
def get_workouts(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    ...
```

### `load_dotenv` (small but important)

`.env` stores secrets:

```env
AUTH_SECRET_KEY=...
AUTH_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Load them in Python:

```py
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
```

Why use an explicit path?

- Your process cwd may be `backend/` or `backend/app/`
- Explicit path makes loading reliable regardless of where you launched uvicorn

Best practices:

- Never commit real `.env` secrets
- Keep `.env` in `.gitignore`
- Provide `.env.example` with dummy keys for teammates

## 10. Auth End-to-End (The Pattern)

### Backend

1. Signup: hash password, store user
2. Login: verify password, return JWT
3. Protected routes: decode JWT via dependency

### Frontend

1. Signup/Login forms call AuthContext methods
2. Save token (`localStorage`)
3. Attach token on every API request (`api` interceptor)
4. Restore session on refresh (read token back into state)
5. Protect private pages (`ProtectedRoute`)
6. Logout clears token + redirects

This exact loop appears in almost every SaaS-style app.

---

## 11. How `page.tsx` Works in Your Home Route

Your home page currently:

1. Marks itself `"use client"` because it uses hooks
2. Wraps content in `ProtectedRoute`
3. Reads `user` from auth context
4. Calls backend: `GET /workouts/workouts`
5. Stores result in typed state: `useState<Workout[]>([])`
6. Renders list (or empty message / error)

Why TypeScript helped here:

```ts
type Workout = {
  id: number;
  name: string;
  description?: string | null;
};

const [workouts, setWorkouts] = useState<Workout[]>([]);
```

Without that type, `useState([])` becomes `never[]`, and using `workout.id` errors.

---

## 12. Recommended Professional Next.js Structure (Growth Path)

As your Workout app grows, aim for something like:

```text
frontend/
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── signup/page.tsx
│   ├── (app)/
│   │   ├── layout.tsx          # authenticated shell
│   │   ├── page.tsx            # dashboard
│   │   ├── workouts/
│   │   │   ├── page.tsx
│   │   │   └── [id]/page.tsx
│   │   └── routines/page.tsx
│   ├── layout.tsx              # root providers
│   └── globals.css
├── components/
│   ├── ui/                     # Button, Input, Modal
│   ├── layout/                 # NavBar, Sidebar
│   └── workouts/               # WorkoutCard, WorkoutForm
├── features/                   # (optional) feature modules
│   └── auth/
│       ├── api.ts
│       ├── AuthContext.tsx
│       └── types.ts
├── lib/
│   ├── api.ts
│   └── auth.ts
└── types/
    └── index.ts
```

Route groups like `(auth)` and `(app)` do **not** appear in the URL. They only organize layouts.

---

## 13. Everyday Best Practices Checklist

### Frontend

- One API client (`lib/api`)
- Keep secrets off the client (only `NEXT_PUBLIC_` for non-secret config)
- Prefer `<Link>` for navigation; `router.push` for post-action redirects
- Put interactivity in Client Components only when needed
- Type shared data (`Workout`, `User`, API responses)
- Handle loading + error states in UI
- Don’t put tokens in plain React state only — persist carefully, clear on logout

### Backend

- Feature routers
- Pydantic schemas for validation
- Dependency injection for DB + auth
- Hash passwords (never store plaintext)
- Explicit CORS origins (not `*` in production with credentials)
- Env-based secrets via `.env` + `load_dotenv`
- Return clear HTTP status codes (`401`, `400`, `201`)

### Compatibility habits

Whenever you add a feature:

1. Write/adjust backend endpoint first (or OpenAPI docs)
2. Confirm request/response in `/docs`
3. Wire frontend call to exact path/method/body
4. Update types on frontend
5. Test signup/login + authorized request

---

## 14. How to Run This Project (Every Time)

### Terminal 1 — Backend

```bash
cd backend
source .venv/Scripts/activate   # Windows Git Bash
cd app
uvicorn main:app --reload
```

- API: http://127.0.0.1:8000
- Swagger docs: http://127.0.0.1:8000/docs

### Terminal 2 — Frontend

```bash
cd frontend
npm run dev
```

- App: http://localhost:3000

### First use

1. Open http://localhost:3000
2. Go to login
3. Sign up
4. Land on home (protected)
5. Workouts list loads from backend (may be empty initially)

---

## 16. Mini Glossary

- **App Router**: Next.js routing system based on the `app/` directory
- **Layout**: Shared UI wrapper around pages
- **Server Component**: Runs on server by default in App Router
- **Client Component**: Browser-interactive component (`"use client"`)
- **Context**: React shared state mechanism
- **Interceptor**: Axios middleware that runs before/after requests
- **JWT**: Signed token proving login identity
- **CORS**: Browser permission rules for cross-origin requests
- **Pydantic schema**: Request/response validation model in FastAPI
- **SQLAlchemy model**: Python class mapped to a DB table
- **Dependency (`Depends`)**: Injected shared logic in FastAPI endpoints

---

## 17. What to Build Next (Practice Plan)

Repeat this loop for each feature:

1. **Backend first**
   - Add schema
   - Add/adjust router endpoint
   - Verify in `/docs`
2. **Frontend second**
   - Add API call in `lib` or feature module
   - Add/adjust page or component
   - Wire loading/error UI
3. **Auth check**
   - Confirm protected endpoints reject missing tokens
4. **Polish**
   - Types, empty states, validation messages

Feature ideas for this app:

- Create workout form
- Delete workout button
- Routines page
- Filter workouts by current user on backend
- Signup page separate from login
- Move remaining `.js` files to `.tsx`


