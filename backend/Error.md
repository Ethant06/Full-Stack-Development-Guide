# 1. What HTTPException does on the backend
When you write:
```
raise HTTPException(status_code=404, detail="Workout not found")
```
FastAPI catches it and turns it into an HTTP response — it does not crash the server. Roughly:

```
HTTP/1.1 404 Not Found
Content-Type: application/json
{"detail": "Workout not found"}
```

# 2. Where it goes
```
get_workout() raises HTTPException(404)
        ↓
FastAPI builds JSON error response
        ↓
Axios in the frontend receives a failed request
        ↓
your catch block reads err.response.data.detail
        ↓
you setError(...) and render it in the UI
```

# 3. Frontend Action to Error

```
const [error, setError] = useState("");
```
```
try {
  await api.get(...) // or post/delete
} catch (err) {
  if (axios.isAxiosError(err)) {
    setError(err.response?.data?.detail || "Something failed");
  }
}
```
```
{error ? <p className="error-text">{error}</p> : null}
```

# 4. Real Example Frontend Endpoint call with Error handling

```
try {
  const res = await api.get("/workouts/", { params: { workout_id: id } });
  setWorkout(res.data);
} catch (err) {
  if (axios.isAxiosError(err) && err.response?.status === 404) {
    setError("Workout not found");
  } else if (axios.isAxiosError(err) && err.response?.status === 401) {
    logout(); // session expired
  } else {
    setError("Failed to load workout");
  }
}
```

# 5. The core HTTP status codes (90% of what you'll deal with)

#### Success

- 200 OK — normal successful response
- 201 Created — successful POST (new resource made)
- 204 No Content — successful DELETE, nothing to send back

#### Client errors (your request is wrong)

-  400 Bad Request — malformed data, missing fields
-  401 Unauthorized — not logged in / bad token
-  403 Forbidden — logged in, but not allowed to do this
-  404 Not Found — route/resource doesn't exist
-  409 Conflict — duplicate resource (e.g. email already taken)
-  422 Unprocessable Entity — data is well-formed but fails validation rules
-  429 Too Many Requests — rate limited

#### Server errors (something broke on the backend)

- 500 Internal Server Error — unhandled crash/exception
- 502 Bad Gateway — server crashed or isn't responding to the proxy
- 503 Service Unavailable — server overloaded/down
- 504 Gateway Timeout — server took too long to respond