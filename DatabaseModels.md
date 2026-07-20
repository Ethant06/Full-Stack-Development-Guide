# Creating Many to Many relationships
When there is a many to many relationships, recall in sql we had to create a junction table between two tables for that relationship. Hence in ORM we need to manually create a table using CORE:

workout_routine_association = Table(
  'workout_routine', Base.metadata,
  Column('workout_id', Integer, ForeignKey('workouts.id')),
  Column('routine_id', Integer, ForeignKey('routines.id'))
)
This serves as the relationship and then later on we actually use orm to create the individual tables in the relationship.
```
class Workout(Base):
  __tablename__ = 'workouts'
  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey('users.id'))
  name = Column(String, index=True)
  description = Column(String, index=True)
  routines = relationship('Routine', secondary=workout_routine_association, back_populates='workouts')

class Routine(Base):
  __tablename__ = "routines"
  id = Column(Integer, primary_key=True, index = True)
  user_id = Column(Integer, ForeignKey('users.id'))
  name = Column(String, index=True)
  description = Column(String, index=True)
  workouts = relationship('Workout', secondary=workout_routine_association, back_populates='routines')
```