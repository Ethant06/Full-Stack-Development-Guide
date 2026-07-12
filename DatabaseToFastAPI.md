# Depends

Dependency is a function that FastAPI runs before our endpoint function, and whose return value gets passed into our endpoint as the input. It is a way to share logic across many endpoints without pasting it into every single on,

 - Example
```
def get_greeting():
  return "Hello!"

@app.get('/greet')
def greet(message: str = Depends(get_greeting)):
  return {"greeting": message}
```
- FastAPI sees the Depends(get_greeting)
- Before running greet(), it calls get_greeting() itself
- Whatever get_greeting() returns ("Hello") gets passed in as message variable
- Then our endpoint function runs with that input
FastAPI calls get_greeting() automatically since it is declared via Depends(...)


# get_db()

```
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
- SessionLocal = sessionmaker(bind=engine). SessionLocal creates a brand new session object, connected to our actual Postgres database through the initial engine we set up.
- db = SessionLocal() simply opens a connection to the actual Postgres database and store it in the variable db.
- When our python code connects to Postgres, Postgres is a running server process and each connection to it, Postgres spins up a dedicated thread on its side to handle that connection and keeps memory allocated for it. It has a hard limit on how many connections it can hold open at once, commonly 100. Every open connection cost real memory and resource on that server.
- We use finally because it guarantees db.close() runs no matter what - even if our endpoint code crashes. This allows it to free up once over and release server-side resources that Postgres allocated when the connetion was opened - so that the slot becomes available for next request. Hence yield/finally dependency pattern is a standard practice, not just style.

# What Depends(get_db) does for a real request
get_db opens the door to our Postgres database.
```
@app.get('/people/{person_id}')
def get_person(person_id: int, db: Session = Depends(get_db)):
    person = db.get(Person, person_id)
    return person
```
- FastAPI see db: Session = Depends(get_Db) so it knows to call get_db() first in order to give result to db parameter
- get_db() is called and inside it, db = SessionLocal runs - real live connection to our actual postgres database opened for this specific request.
- get_db() reaches yield db - it hands that live session object over to FastAPI, which plugs it into get_person's db parameter.
- Now get_person runs: db.get(Person, person_id) - this uses the real session to actually query our real people table in Postgres.
- get_person returns the person. FastAPI is now done with the endpoint
- FastAPI goes back to the paused get_db() function, which resumes right after yield, hitting db.close() - this closes up that specific connection, freeing it.


# Effectiveness of get_db() depends Function

- Without get_db:
```
@app.get('/people/{person_id}')
def get_person(person_id: int):
    db = SessionLocal()
    person = db.get(Person, person_id)
    db.close()
    return person
```

- With get_db

```
@app.get('/people/{person_id}')
def get_person(person_id: int, db: Session = Depends(get_db)):
    person = db.get(Person, person_id)
    return person
```

