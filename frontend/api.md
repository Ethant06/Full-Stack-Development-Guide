- Our FastAPI backend is a separate program running on our computer (server) listening on port 8000 and it sits there waiting for incoming requests. Our Next.js frontend is completely different program running in the browser that needs to send messages to that backend to get data.

## Async/Await - Better way to write Promise Code
Rather than chaining .then(), JS lets us write asynchronous code that looks synchronous:
```
async function getRoutines() {
  const response = await fetch("http://localhost:8000/routines/");
  const data = await response.json();
  console.log(data);
}
```
- async means "this function will do asynchronous work and return a promise"
- await means "pause here until this Promise resolves, and then continue with the actual value.

## Where fetch() gets annoying and how Axios Helps
- If our backend returns a 404 error, Fetch() does not throw an error for 404, 401, 500, only throws if the network itself fails(no internet, DNS failure). So with fetch, we will always have to manually check if response is good.
- Axios fixes this by automatically treating any non-2xx status code as an error:
```
try {
  const response = await axios.get("http://localhost:8000/routines/999");
  // only reaches here if status was 200-299
} catch (error) {
  console.log(error.response.status); // 404
  console.log(error.response.data);   // whatever error detail FastAPI sent back
}
```

## AXIOS USAGE

```
import axios from "axios";

const response = await axios.get("http://localhost:8000/routines/");
console.log(response.data); // already parsed JSON
```

For POST with a body:
```
const response = await axios.post("http://localhost:8000/auth/signup", {
  username: "alice",
  password: "secret123",
});
```

## Why we need a shared instance
Imagine every file in our app talks to our backend like ths:
```
axios.get("http://localhost:8000/routines/", {
  headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
});

axios.get("http://localhost:8000/workouts/", {
  headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
});

axios.post("http://localhost:8000/routines/", newRoutine, {
  headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
});
```
So we can do
```
const api = axios.create({
  baseURL: "http://localhost:8000",
})
```
Now we can just write:
```
api.get("/routines/")
```
Then anywhere in our app we want to hit the backend, we will do
```
import api from "/lib/api"
api.get("/routines/)
```
## Interceptors - automatically modifying every request
```
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```
- api.interceptors.request.use(callback) - registers a function that runs on every request
- config describes request about to be sent like URL, headers, method, body
- localStorage.getItem("token") reads whatever token we saved (from login()) out of browser storage. localStorage is a key-value store built into every browser that persists even when we close the tab or refresh the page.
- config.headers.Authorization = `Bearer ${token}` this line changes the outgoing request, adding an Authorization header before it is sent.
- return config - required and whatever config we return becomes the actual request axios sends.
# We set this up once. When our app first loads and api.js gets imported, all it does is register a rule with Axios: before sending anything through api, run this function first. We never call this function by name anywhere else in the code.
- This interceptor always matters because without the interceptor we would have to write this every single time on every page for every request:
```
const token = localStorage.getItem("token");
const response = await axios.get("http://localhost:8000/routines/", {
  headers: { Authorization: `Bearer ${token}` }
});
```
With interceptor we just write:
```
const response = await api.get("/routines/");
```
And the token gets attached automatically behind the scenes.

# Full lib/api.js code
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
const api = axios.create({
  baseURL: "http://localhost:8000",
});

axios.create({...}) makes a customized copy of Axios — not the global one, a new object called api. baseURL means: every request made through api automatically gets http://localhost:8000 glued onto the front of whatever path you give it. So api.get("/routines/") really sends a request to http://localhost:8000/routines/.

api.interceptors.request.use((config) => {

Registers a function that Axios will automatically run before every single request sent through api — you never call this function yourself, Axios calls it for you, every time.

  const token = localStorage.getItem("token");

localStorage is the browser's persistent storage — data saved here survives page refreshes and closing the tab (unlike a normal JS variable). This line checks: "is there a saved login token from a previous successful login?"

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

config represents the outgoing request that's about to be sent (its URL, headers, body, etc). If we found a token, we attach it as an Authorization header, in the exact format (Bearer <token>) your FastAPI backend's get_current_user function expects to receive and decode.

  return config;
});

Required — whatever config we return becomes the actual request that gets sent. If we forgot this line, the request would break.

export default api;

Makes api importable from other files: import api from "../lib/api".

Purpose of this file, one sentence

Build one shared, pre-configured "messenger" (api) that (1) always knows your backend's base address, and (2) automatically attaches your saved login token to every request — so you never repeat either of those two things anywhere else in your app.









