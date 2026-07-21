# deps.py for dependencies

The idea of a deps.py file is to be a central place for things that many of our app routes will need repeatedly:
- A database session (get_db)
- The current authenticated user (get_current_user)
- Permission checks (require_admin)

Hence rather than each route file like workouts.py or routines.py redefining get_db() or the password hasher, they all just do
```
from .depds import db_dependency, oauth2_bearer_dependency
```

### Benefits of this practice

- Avoids duplication
- Single source of truth: if we ever change how sessions are created or rotate our JWT algorithm, we edit one rather than several.
- Our route files stays focused on business logic rather than setup code.