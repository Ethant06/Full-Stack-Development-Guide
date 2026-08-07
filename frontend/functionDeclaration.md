# 1. Use arrow functions for everything except the component itself

```
// Event handlers, helpers, callbacks
const handleCreate = async (e) => { ... };
const loadWorkouts = async () => { ... };
const handleDelete = (id) => { ... };
```

# 2. Use function declarations for components
```
// Conventional for the component
function HomeContent() { ... }
export default function Home() { ... }
```

# 3. Use the shorthand arrow form for simple one-liners

```
onChange={(e) => setName(e.target.value)}
onClick={() => handleDelete(workout.id)}
```

# 4. Arrow functiosn in callbacks(.map, .filter, event handlers) over function expressions.
A callback function is a function that you pass as an argument into another function, which is then executed inside that outer function at a later time.
```
workouts.map((workout) => <li key={workout.id}>...</li>)
```
- workouts — the original array of workout objects
- .map(...) — "for every workout in this array, do something with it, and collect the results"
- (workout) => <li key={workout.id}>...</li> — the callback we just talked about. workout here is one single item from the array, on each pass — not the whole array

So conceptually, if workouts has 3 items, .map() calls this arrow function 3 separate times, once per workout, each time with a different workout object. The result is a brand new array with 3 <li> elements in it — one per workout.