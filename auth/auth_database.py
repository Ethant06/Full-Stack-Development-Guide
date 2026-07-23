from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/workout_app"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

def get_db():
  db = SessionLocal
  try:
    yield db
  finally:
    db.close()

Base = declarative_base( )