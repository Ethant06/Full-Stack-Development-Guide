from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, utils
from auth_database import get_db, Base, engine
import models
import os
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta, timezone


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

Base.metadata.create_all(bind=engine)

#Helper function that takes user data
def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({'exp': expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

app = FastAPI()

@app.post('/signup')
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

  #check if user exist or not
  existing_user = db.query(models.User).filter(models.User.username == user.username).first()
  if existing_user:
    raise HTTPException(status_code=400, detail='Username already exist')

  #Hash the password
  hashed_pass = utils.hash_password(user.password)

  # Create new user instance
  new_user = models.User(
    username = user.username,
    email = user.email,
    hashed_password = hashed_pass,
    role = user.role
  )

  #save user to database
  db.add(new_user)
  db.commit()
  db.refresh(new_user)


  #return the value (except password)
  return {'id': new_user.id, 'username': new_user.username, 'email': new_user.email, 'role': new_user.role}

