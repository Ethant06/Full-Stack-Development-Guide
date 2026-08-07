# useEffect or known as Side Code

- A tool for running code that reacts to the outside world (API, the DOM, brower storage).
- We use this whenever code needs to run automatically without a user clicking anything -
###### If nobody has to click anything for this code to run, it's useEffect.
###### Synatx Shape
```
useEffect(function, [dependencies])
1. useEffect(() => {}) - reruns after every re-render
2. useEffect(() => {}, []) - runs only on mount - one and done effect. Suppose to we add eventListeners when the DOM changes. Without useEffect, it will add 1000 eventListeners
3. useEffect(() => {}, [value]) - side code runs on mount + when value changes
```
###### Uses
- Event listeners
- Dom manipulation
- Subscriptions
- Fetching data from an API
- Clean up when a component unmounts(removing component from DOM)

###### Example Usage
```
 const loadWorkouts = async () => {
    const response = await api.get<Workout[]>("/workouts/");
    setWorkouts(response.data);
  };

 useEffect(() => {
    const fetchWorkouts = async () => {
      try {
        await loadWorkouts();
      } catch (err) {
        if (axios.isAxiosError(err)) {
          setError(err.response?.data?.detail || "Failed to load workouts");
        } else {
          setError("Failed to load workouts");
        }
      }
    };

    fetchWorkouts();
  }, []);
```
- useEffect is what makes the workout list show up automatically once the moment the page opens, instead of staying empty forever.
- Without it, workouts would just sit at its initial value ([]) — nothing would ever go fetch the real data from the server, and the user would land on the page seeing "No workouts yet" even if they actually have 20 saved workouts sitting in the database. There'd be no button to click to trigger the fetch either, since loading your own data isn't something a user should have to manually ask for — it should just be there when the page opens.
- So its one job is: the instant this page mounts, go get the real workout data and put it on screen, and if that fails, show an error instead of leaving things silently broken.
- Everything after that initial load — adding a workout, deleting one — is handled separately, by the event handlers

# Start Transition

startTransition lets you say "this particular batch of updates is low priority — if something more urgent comes in (like a keystroke), handle that first and let this wait."

A classic example (where it's most commonly taught)
```
const [query, setQuery] = useState("");
const [results, setResults] = useState([]);

function handleChange(e) {
  setQuery(e.target.value); // urgent — keep the input responsive

  startTransition(() => {
    setResults(filterHugeList(e.target.value)); // not urgent — can lag a bit
  });
}
```
Here, typing into the search box (setQuery) stays instantly responsive, while filtering a huge list (setResults) — which might be slow — doesn't block or freeze the input while it catches up. React will interrupt the transition update if you type another character before it finishes.