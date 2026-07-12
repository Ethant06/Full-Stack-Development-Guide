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