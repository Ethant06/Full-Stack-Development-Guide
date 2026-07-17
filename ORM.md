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

# Overall
- ORM maps Python classes to tables (Base, declarative_base()), where each instance is a real row you manipulate like a normal object; relationship() + back_populates lets you navigate joins as attributes instead of writing them.
- Session - the ORM manager - tracks objects, detects changes, and translates them into SQL at commit() time. It can also run raw SQL but that bypasses ORM machinery entirely.
