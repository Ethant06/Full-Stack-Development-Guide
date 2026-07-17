# Endpoint Checking

To test out how some endpoints work, we can create our api endpoints and the functions
and go to localhost/docs to view our endpoints and test them with example inputs

# Type Implementation

Everytime we create a function with a parameter for an endpoint, we should declare
the type of the paramter whether it is an int, string, dict, etc.

# API Endpoint Summary

An endpoint is just a URL that your frontend (or another client) can send an
HTTP request to.

## The URL (Path)

The path identifies what resource you're working with. Some examples are
  /todos,
  /users,
  /books

## The HTTP Method

The HTTP method tells the server what operation to perform on that resource.

GET, POST, PUT, PATCH, DELETE. The same path can have different methods so there
can be get(/todos), post(/todos), delete(/todos). The HTTP method changes while the
path never changed.

## Path Parameters

Use path parameters when identifying which specific resource you want. Example
of an endpoint would be get(/todos/{todo_id}). The request would be something like
GET/todos/5 and the FastAPI would extract todo_id = 5.

## Query Parameter

Query parameters come after a ? in the URL. An endpoint would be
def get_todos(first_n: int = None). And we request would be GET/todos?first_n=5.
Query parameters do not identify a resource, rather they modify the request for
filtering, searching, sorting, and limiting results.

# HTTPException

HTTPException comes from fastapi. Say an endpoint is suppose to return a result
if it finds a match in the clients input. If there is no match, we could return something
like 'None', which would be a 200 OK with empty body, lying to the client. HTTPException lets
us stop the execution and return a proper HTTP error with a real status code and JSON error.
FASTAPI captures an exception and converts it to a response like {"detail": "Todo not found}
with a 404 status code.

# Response_model =
Validates/filters the single returned object. Without response_model, FastAPI would just serialize whatever we return, including sensitive information if we ever dont intend to include such as password hash - leading to leaks.

```
@app.get('/todos/{todo_id}', response_model=Todo)
```

This is a second independent schema layer, separate from the input schema like TodoCreate.

- This validates the outgoing response agaisnt the given schema before sending it. If
our function accidentally returns something missing a required field, FastAPI raises a server error rather than sending malformed data to the client.
- Filters the response. Only fields defined on the response_model are presented, even though
the object we return has extra attributes like age. This is great for security because
later if our endpoint function returns more data that might be sensitive like a password
that is not on the response_model declaration, response_model won't leak it unless the attribute is explicitly part of the response_model schema. So in short, response_model
fixes what exactly is returned and does not include any other things.
