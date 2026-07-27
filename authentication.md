```
1. POST /login
   Body: username=john&password=mypass
   ─────────────────────────────────────
   → handled by OAuth2PasswordRequestForm
   → server verifies credentials, issues a JWT
   ← Response: {"access_token": "eyJ...", "token_type": "bearer"}

2. GET /users/me
   Header: Authorization: Bearer eyJ...
   ─────────────────────────────────────
   → handled by OAuth2PasswordBearer
   → server extracts + verifies the token
   ← Response: {"username": "john"}

3. GET /workouts
   Header: Authorization: Bearer eyJ...
   → same OAuth2PasswordBearer handles this too, and every future protected route
```

# OAuth2PasswordRequestForm
Is used on login routes and this class parses the username and the password form the form body and creates a class that we can obtain those attributes from to check with our database.

# OAuth2PasswordBearer
This is for step 2 after the user successfully logins. Once user logins, it no longer needs username/password again, rather it needs to check the users token it got after logging in. This token is checked on future requests and this class main job is to parse the token out of the authentication header.