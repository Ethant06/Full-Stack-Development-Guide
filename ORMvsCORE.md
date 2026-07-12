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