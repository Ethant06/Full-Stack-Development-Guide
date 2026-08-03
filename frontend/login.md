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