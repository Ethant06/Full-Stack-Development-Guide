# Problem that Context Solves
- Once a user logs in, many different components need to know if someone is logged in and who - your navbar to show "Logout" vs "Login", your protected pages to decide whether to let someone in, your routines page to know whose routines to fetch.

- Without context, we would have to store user in our top level page and mass it down as a prop to every single component. Context solves this by letting us put a piece of state in a global closet that any component anywhere in our app can open and grab from.

# CreateContext
```
import { createContext } from "react"

const AuthContext = createContext();
```
Creates an empty container. This does nothing yet, needs something to put stuff into the box(Provider) and something to take stuff out of the box(useContext)

#### Provider
```
export const AuthProvider = ({ children }) => {
  // ... state and functions go here

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
```
Now whatever JSX we put between opening and closing tags of this component becomes children:
```
<AuthProvider>
  <somePage />
</AuthProvider>
```
- somePage is the children inside AuthProvider
- <AuthContext.Provider value
- Whatever we put in value = {{..}} becomes available to any component wrapped inside it, via useContext(AuthContext)

# Where it lives

```
frontend/
  app/
    layout.js
    login/
      page.js
  context/
    AuthContext.js     ← this file
  lib/
    api.js
```

##### There are exactly two places this file gets used in our app

- 1.
```
// app/layout.js
import { AuthProvider } from "../context/AuthContext";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
```
Here {children} means literally every page in our entire app - homepage, login page, routines page. By wrapping all of it inside <AuthProvider>, we are saying: every single page in this app is allowed to access user, login, and logout.

- 2. any page/component that needs user, login, or logout.
