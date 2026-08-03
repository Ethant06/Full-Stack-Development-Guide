from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, utils
from auth_database import get_db, Base, engine
import os
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jwt import PyJWTError

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

Base.metadata.create_all(bind=engine)

# Helper function that takes user data
def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({'exp': expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=[ALGORITHM])
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

# verifies that user successfully logins and creates a unique access token for them accordingly
@app.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.username == form_data.username).first()

  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Username')

  if not utils.verify_password(form_data.password, user.hashed_password):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")

  token_data = {'sub': user.username, 'role': user.role}
  token = create_access_token(token_data)
  return {'access_token': token, "token_type": "bearer"}


# this checks the token, like checking a person with a badge in the building who wants to enter a room
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(token: str = Depends(oauth2_scheme)):
  credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credential")
  headers=({"WWW-Authenticate": "Bearer"})

  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    username: str = payload.get("sub")
    role: str = payload.get("role")
    if username is None or role is None:
      raise credential_exception

  except PyJWTError:
    raise credential_exception

  return {"username": username, "role": role}


@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
  return {"Message": f"Hello, {current_user['username']} | You accessed a protected route"}

def required_roles(allowed_roles: list[str]):
  def role_checker(current_user: dict = Depends(get_current_user)):
    user_role = current_user.get("role")
    if user_role not in allowed_roles:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permission")
    return current_user
  return role_checker


@app.get("/profile")
def profile(current_user: dict = Depends(required_roles(["user", "admin", "Engineer"]))):
  return {"message": f"Profile of {current_user['username']} ({current_user['role']})"}


@app.get("/user/dashboard")
def user_dashboard(current_user: dict = Depends(required_roles(["user"]))):
  return {"Message": "welcome User"}

@app.get("/admin/dashboard")
def user_dashboard(current_user: dict = Depends(required_roles(["admin"]))):
  return {"Message": "welcome Admin"}