# What is JSX

```
return (
  <div className="container">
    <h2>Login</h2>
  </div>
);
```
- JSX is a syntax extension that gets compiled into plain JavaScript function calls.
- Every JSX expression must return one single root element (hence wrapped in <div>)

# What is a component

- A component is just a JavaScript function that returns JSX which becomes UI.
```
function Greeting() {
  return <h1>Hello!</h1>;
}
```
- 1. UI components (usually return visible JSX)
NavBar, login form, workout list
- 2. Wrapper / logic components (may return children or null)
AuthProvider wraps the app and provides data
ProtectedRoute either shows children or redirects
###### A component is a function: take inputs (props/state) → optionally run logic → return JSX (or null). Export it only if another file needs it.

# What is useState

Normal JavaScript variables dont cause the page to update when they change. If we did:
```
let username = " ";
username = "alice"; - the page does not re-render automatically
```
- React needs a special mechanism to say "this variable value affects the UI so redraw it when it changes. That is useState:
```
const [username, setUsername] = useState(");
```
- useState("") creates one piece of state, starting at an empty string ""
- It returns an array with exactly two things: the current value (username) and a function to udate it (setUsername)


# Building pieces

### Skeleton Basic
```
"use client"

import { useState } from "react";

export default function Login() {
  return (
    <div>
      <h2>Login</h2>
    </div>
  );
}
```
- "use client" tells Next.js this component needs to run in the browser (which is needed anytime we use useState, onClick, form input, etc - anything interactive)

### Login form
```
"use client";

import { useState } from "react";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  return (
    <div>
      <h2>Login</h2>
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
    </div>
  );
}
```
- value={username} - this ties the box's displayed text directly to our username state. Whatever username currently equals, that's what shows in the box.
- onChange={...} - this runs every single time the user types a character or deletes one.
- (e) => setUsername(e.target.value) - this is an arrow function where e is the event object the browser gives us automatically whenever something happens (a click). e.target is the actual <input> DOM element that triggered the event so e.target.value is whatever text input typed in the box.

Hence full loop is:
```
1. User types "a" into box
2. Browser fires onChange, giving us event e.
3. e.target.value is "a"
4. We call setUsername("a")
5. React re-runs the component. username is now "a".
6. The <input value={username}> re-renders showing "a" in the box
```

### Login Submission

```
"use client";

import { useState } from "react";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Submitting", username, password);
  };



  return (
    <div>
      <h2>Login</h2>
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
- <form onSubmit={handleSubmit}> - normally submitting an HTML form causes the whole browser page to reload. But we dont want that. We want to handle the submission with Javascript instead.
- e.preventDefault() - this is the line that stops that default full-page-reload behavior, letting us handle the submit ourselves.
- <button type="submit"> - clicking this button or pressing Enter in the form triggers the form's onSubmit.


