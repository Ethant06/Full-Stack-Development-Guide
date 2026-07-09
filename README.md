# Starting a Project

- Overall, we will create a frontend/ and a backend/ along with a README.md and a .gitignore
as the main project structure

## Backend
- Create and CD into backend/ and create a virtual environment. Python -m venv .venv and this will create backend/.venv/. We need this virtual environment so that each project we make has its own packages rather than conflicting with other projects.

- Activate the virtual environment and download dependencies/packages. After downloading,
we will pip freeze > requirements.txt so that all the downloads we did will be recorded into requirements.txt file that we create. This allows it so that anyone can recreate our environment with 'pip install -r requirements.txt.

## Frontend

- CD .. and command 'npx create-next-app@latest frontend, which will install all the packages and creates frontend/.

- Then install npm

# Running Everything

Open two terminals

- Terminal 1
```
cd backend and activate virtual environment.
Then uvicorn app.main:app -- reload where :app is the variable name of fastAPI()
localhost:8000
```

Terminal 2
```
cd frontend and npm run dev
localhost:3000
Now the frontend can send requests via http://localhost:8000/chat for instance.
```

# How they communicate

### React
```
fetch("http://localhost:8000/chat", {
  method: "POST",
  body: JSON.stringify(data)
})
```

### FastAPI
```
@app.post("/chat")
def chat():
  ...
```


# Packages Commonly Installed

Backend (Python):

- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- Alembic (database migrations)
- python-dotenv (load environment variables)
- LangChain or other AI frameworks (if needed)
- OpenAI SDK or other model providers

Frontend (Node):

- Next.js
- React
- Tailwind CSS
- Axios (optional; fetch is built into modern browsers and Next.js)
- shadcn/ui (component library)
- Lucide React (icons)