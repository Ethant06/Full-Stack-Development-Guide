# Setup

```
Base = declarative_base()
```
This creates the base class that all ur ORM model classes must inherit from - the thing that turns a normal Python class into one that SQLAlchemy recognizes as "this maps to a database table".

```
class Person(Base):
  __tablename__ = "people"
  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
```
- By inheriting from Base, our Person class gets a special behavior:
- SQLAlchemy scans its class attributes (id, name) and understands them as table columns, not just normal Python attributes.
- __tablename__ tells it which actual database table this class maps to
- Base keeps an internal registry of every class that inherits from it - this is how it knows about all our models collectively. This is similar to MetaData in 'Core' but instead of manually building Table objects and passing 'meta' into each one ourself, Base does that bookkeeping for us as a side effect of just defining normal-looking Python classes.

## Session — ORM usage (the version you'll actually use most)

session = Session(engine)

new_person = Person(name="Mike", age=30)
session.add(new_person)
session.commit()

session.query(Person).filter(Person.name == 'Mike').first()
session.get(Person, person_id)

person.age = 50          # just mutate the attribute
session.commit()          # Session detects the change, issues UPDATE automatically

session.delete(person)
session.commit()

## Relationships — one-to-many

class Person(Base):
    ...
    things = relationship('Thing', back_populates='person')

class Thing(Base):
    ...
    owner_id = Column(Integer, ForeignKey('people.id'))
    person = relationship('Person', back_populates='things')

back_populates keeps both sides in sync — each side must name the attribute
on the OTHER class. Lets you do bob.things (list of Thing objects) instead
of writing a manual join.

## Relationships — many-to-many (needs a Core-style association Table)

workout_routine_association = Table(
    'workout_routine', Base.metadata,
    Column('workout_id', Integer, ForeignKey('workouts.id')),
    Column('routine_id', Integer, ForeignKey('routines.id'))
)

class Workout(Base):
    ...
    routines = relationship('Routine', secondary=workout_routine_association, back_populates='workouts')

This is the one standard exception where a plain Table (Core-style) is still
used inside ORM code — junction tables with no data of their own don't need
a full class. You never query this Table directly; relationship(secondary=...)
manages it for you.

# Overall
- ORM maps Python classes to tables (Base, declarative_base()), where each instance is a real row you manipulate like a normal object; relationship() + back_populates lets you navigate joins as attributes instead of writing them.
- Session - the ORM manager - tracks objects, detects changes, and translates them into SQL at commit() time. It can also run raw SQL but that bypasses ORM machinery entirely.
