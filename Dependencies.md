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



# Actual Dependencies Functions

### 1. Bcrypt (Password hashing) - How to store passwords safely
This solves a storage problem and has nothing to do with loggin in - purely about what sits in our database. Touches database and happens at signup and at moment of login verification.
- When a user sign up, we never store their raw password.
- Instead we run it through bcrypt which turns it into a scrambled irreversible string like a #9*asjnasjdn%$$asj.
- Then on login, we don't unhash the stored value, - we hash the password they just typed and check if it matches the irreversible string.
- Hence then if our database ever leaks, attackers get useless scrambled strings.


### 2. OAuth2 Password Flow - Process/Protocol for logging in (CONCEPTUAL BUT IS A SPEC AND HAS IMPLEMENTATION)
This is the process/spec, not code or a technology. It describes a sequence of steps:
- Cliet sends username + password to a token endpoint e.g. POST/auth/token
- Server checks credentials (this is where bcrypt gets used to verify)
- If valid, server then issues an access token back to the client
- The client stores that token and sends it in the authorization header on every future request.
- Server checks header on protected routes to know who is asking everytime onward.

#### For password flow, what is a Header?
Every HTTP request isn't just a URL, it is a URL plus a bunch of extra metadata called headers. Authorization: Bearer '<token>' is one header among many and this is mainly for proof of identity on every request.
- When the user enters credntials and server checks the credentials (bcrypt), it builds a JWT token and sends it back. That is the server's job for login and it is done - it does not save this token on the server side since with JWT, it does not keep a record of who is logged in.
- Then the client stores that token - meaning the frontend app or mobile app, whoever is calling your API takes that token and holds onto it somewhere like localstorage or a secure storage in a mobile app. THis is all client-side respnsibility.
- Then everytime the user wants to say see its workout, the client makes a separate HTTP request with no username/password this time. The client just attaches the token it saved onto this request in that Authroization header and will do it for every request like get workouts, create routine, delee a workout, etc - until the token expires of the user logs out.
- The server checks the headers on protected routes.
###### Overall in old-school web apps (session-based auth), the server would remember that the user say "John logged in" by storing a session ID somewhere. But with JWT and OAuth2 bearer tokens, the server remembers nothing between requests and each request holds everything such as the toen to prove the identity to the server. An analogy is you enter a building and they put a wristband on your wrist (client storing token.) Then everytime you walk through different door or areai n the buildings, the guards at the door just look at your wrist rather than ask for your ID again.


### 3. JWT (JSON Web Token)
This is one common way to implement the "access token" that OAuth2 password flow says we need to issue.
- JWT is a string with three parts (header, payload, signature) which contains data inside,
is signed with our SECRET_KEY so the server can verify it was not tampered with, and is not encrypted by default.
- When a request comes in with a token, our server decodes it and checks the signature is valid using SECRET_KEY and if so then it trusts the data inside like this is user#5.

# How they all fit together for login

### 1. User submits username and password

### 2. Server looks up the user, hashes the submitted password and compares to stored hash
This step uses bcrypt

### 3. If it matches, server creates a token containing user information, signs it with SECRET_KEY.
This step creates a JWT

### 4. Server returns the JWT to the client.
OAUTH2 password flow "issue access token" step

### 5. Client sends that JWT on every future request in the Authorization header.
Use token step in OAuth2.

### 6. Server decodes/verifies the JWT signature to identify the user
This uses JWT verification.