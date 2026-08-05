Without a ProtectedRoute, this is what happens if a logged-out user visits a protected route intended for logged in users only:
1. The page renders
2. It tries to fetch data: api.get("/routines/")
3. No access token exists -> interceptor sends the request without one -> FastAPI rejects with 401.
4. Our page has to somehow handle that error - showing a blank screen, an error message, or a broken UI, since it exected routine data that never came.

#### Protected Route Functionality
This prevents that broken/ugly state by catching the problem before the page even tries to ftch anything - redirecting cleanly to /login instead. So although this is not a strict requirement, it is an effective UX requirement for any real app.

## Where it should live
```
frontend/
├── app/
│   ├── layout.js
│   ├── login/
│   │   └── page.js
│   └── routines/
│       └── page.js          ← uses ProtectedRoute
├── components/
│   └── ProtectedRoute.js    ← lives here
├── context/
│   └── AuthContext.js
└── lib/
    └── api.js
```
This goes in a components/ folder - a place for reusable pieces of UI/Logic that arent full page themselves but gets used inside pages.

## The Full Code
```
// components/ProtectedRoute.js
"use client";

import { useContext, useEffect } from "react";
import { useRouter } from "next/navigation";
import AuthContext from "../context/AuthContext";

const ProtectedRoute = ({ children }) => {
  const { user } = useContext(AuthContext);
  const router = useRouter();

  useEffect(() => {
    if (!user) {
      router.push("/login");
    }
  }, [user, router]);

  return user ? children : null;
};

export default ProtectedRoute;
```

## How it fits into the whole login system

###### 1. Visitor arrives not logged in yet
app/layout.js wraps the whole app in <AuthProvider> -> user starts as null (from useState(null) in AuthContext.js)

###### 2. Visitor tries to go to /routines directly
```
// app/routines/page.js
import ProtectedRoute from "../../components/ProtectedRoute";

export default function RoutinesPage() {
  return (
    <ProtectedRoute>
      <h1>Your Routines</h1>
    </ProtectedRoute>
  );
}
```
ProtectedRoute runs, see user is null, and its useEffect fires router.push("/login)

###### 3. Visitor lands on /login, then logs in
app/login/page.js then calls login(username, password) from AuthContext.js and then gets back a token and saves it to localStorage and calls setUser({ token: access_token })

###### 4. User changes from null to a real object
AuthProvider wraps the entire app so this state user is visible everywhere instantly.

###### 5. Visitor now navigates to /routines again
ProtectedRoute runs its check again and now useContext(AuthContext) returns a real user object, so user is truthy and now returns the children

