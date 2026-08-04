# The folder Skeleton

```
frontend/
├── app/
│   ├── layout.js          ← wraps entire app in AuthProvider
│   ├── page.js             ← homepage
│   └── login/
│       └── page.js         ← the login form
├── context/
│   └── AuthContext.js      ← global "who is logged in" state + login/logout logic
└── lib/
    └── api.js              ← configured Axios instance, used for ALL backend calls
```
- lib/api.js — the tool that physically sends requests to your FastAPI backend.
- context/AuthContext.js — uses that tool to log in/out, and stores the result (user) somewhere the whole app can read.
- app/login/page.js — the UI the user interacts with; it doesn't talk to the backend itself, it just calls functions from AuthContext.js.
- app/layout.js — glues AuthContext.js onto your entire app so every page can access it.

## lib/api.js
Purpose is build one shared messenger (api) that knows our backend base address and automatically attaches our saved login token to every request - so we dont repeat anywhere else in our app when calling api.
```
// lib/api.js
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```
- Interceptors registers a function that Axios automatically run before every single request sent through api.
- LocalStorage here is the browser's persistent storage, and that token line checks if there is a saved login token from the previous successful login. Then there are three cases of this interceptor throughout the whole app. 1. If we request login api without any token, then the interceptor runs and sends the request header-less, which is as expected as then the login endpoint fastapi will create us the token after we login. 2. Calling a protected endpoint before loggin in. If someone accidentally triggers api.get(/routine/) without ever logging in, the interceptor will run, find no token in localStorage, and still send the request, but without a header - then in the backend FastApi, OAuth2PasswordBearer will obtain the request header and pass it into get_current_user authentication, and it will reject the entire request before even moving onto /routine endpoint. 3. If localStorage has a token saved and we called an endpoint request like api.get("/routines/"), our get_curent_user will validate it and pass on the parameters like username onto the endpoint we wanted to call.
- config is returned, and whatever config we return becomes the actual request that gets sent.

## context/AuthContext.js

```
// context/AuthContext.js
"use client";

import { createContext, useState } from "react";
import { useRouter } from "next/navigation";
import api from "../lib/api";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const router = useRouter();

  const login = async (username, password) => {
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    const response = await api.post("/auth/login", formData, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });

    const { access_token } = response.data;
    localStorage.setItem("token", access_token);
    setUser({ token: access_token });
    router.push("/");
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
    router.push("/login");
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
```
- const login - using the api object imported from lib/api.js. Combined with baseURL, this sends a POST request to http://localhost:8000/auth/login, with formData as the body, and this explicit header telling the server "this body is form-encoded" (overriding Axios's default of assuming JSON)
- localStorage.setItem - Saves the token in the browser's persistent storage, so lib/api.js's interceptor can find and reuse it on every future request — and so it survives page refreshes.
- setUser({ token: access_token }); The core moment — flips user from null to a real object. Everywhere in your app using useContext(AuthContext) to read user will now see this new value and re-render accordingly (e.g. ProtectedRoute will stop redirecting, Navbar can show "Logout" instead of "Login").
- Return: This is the "filling the box" step. value={{ user, login, logout }} — this exact object is what any component gets back when it calls useContext(AuthContext). So now every page or any file we go to, we can derive login/logout function from AuthContext (container).
#### Two returns
- 1. Default export - export default AuthContext is the empty box itself used by any component that wants to read from context. login/page.js needs this for instance.
- 2. AuthProvider - the component that fills the box and wraps our app with it. Used once in layout.js <AuthProvider>Children</AuthProvider>. Named export


## app/login/page.js
```
// app/login/page.js
"use client";

import { useContext, useState } from "react";
import AuthContext from "../../context/AuthContext";

export default function Login() {
  const { login } = useContext(AuthContext);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await login(username, password);
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed");
    }
  };

  return (
    <div>
      <h2>Login</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}
```
Displays a form, collect what the user types, and - on submit - hand that data off to login() (from AuthContext.js) without needing to know anything about HTTP, tokens, or your backend directly.

# Full Flow:
- app/login/page.js — user types credentials, clicks submit → handleSubmit runs → calls login(username, password).
- context/AuthContext.js — login function runs: builds form data, then calls api.post("/auth/login", formData, {...}).
- lib/api.js — the api object combines baseURL + /auth/login into the full address, and (via the interceptor) checks for an existing token to attach — finds none yet at this stage.
- Axios physically sends the request to your FastAPI backend, which checks the database, verifies the password, and returns {access_token, token_type}.
- Back in context/AuthContext.js — the response is caught by await, the token is extracted, saved to localStorage, and setUser(...) updates the global "logged in" signal. The user is redirected to /.
- Any other component anywhere in your app (Navbar, ProtectedRoute, etc.) reading user via useContext(AuthContext) automatically re-renders, now seeing the logged-in state.
- From this point on, any future api.get(...) or api.post(...) call — from any file — will have the saved token automatically attached by the interceptor in lib/api.js, without you writing that logic again.