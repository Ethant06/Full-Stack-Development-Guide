# Difference

## Core

- What represents a table: A table object

```people = Table(
  "people",
  meta,
  Column('id', Integer, primary_key=True),
  Column('name', String, nullable=False),
  Column('age', Integer)
)
```
- What represents a row: A raw row returned from query.

- How to query: people.select().where(people.c.name == 'Bob')

- What manages it: Connection

## ORM

- What represents a table: A python class
```
class Person(Base):
  __tablename__ = "People"
```
- What represents a row: An actual instance of our class:
```
bob = Person(name="Bob") - a real python object
```
- How to query:
```
session.query(Person).filter(Person.name == 'Bob)
```
- What manages it: Session


# Overall

- Core describes tables as Python Objects (Table, Column) and builds SQL statements via method chaining (.select(), .join(), .group_by()) - we still think in terms of tables and statements.

- ORM maps Python classes to tables and each instance is a real row that you can manipulate with relationship() + back_populates to navigate joins as attributes instead of writing them.

### Connection - Core, raw/low-level for queries
```
conn = engine.connect()
conn.execute(text("INSERT INTO people (name, age) VALUES ('Mike, 30)"))
conn.commit()
```
- This sends SQL, get back raw rows.
- No concept of objects, just data in and data out
- Can also be used higher level with Table/Column style code - people.select(), .join(), etc.

### Session - ORM, object-aware for queries
```
session = Session(engine)
new_person = Person(name="Mike", age=30) <- an actual Python Object
session.add(new_person)
session.commit()
```
- Tracks real python objects (Person instances), not just raw rows
- Detects changes to those objects automatically: person.age = 50 -> commit() generates the update for us.
- Manages relationships() - Ethan.things gives you related objects without manual joins
- Internally still uses a Connection to actually talk to the database - Session just wraps around connection-level SQL execution with object-tracking on top.