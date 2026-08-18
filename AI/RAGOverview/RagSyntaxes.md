- Prompt — the actual text you send to the LLM. It's just a string.
- kwargs - a dictionary that packages up everything needed to call the LLM:
```
kwargs = {
    "prompt": "Explain recursion to a beginner.",
    "temperature": 0.2,
    "max_tokens": 500
}
```
- **kwargs:
```
def call_llm(prompt, temperature, max_tokens):
    ...
Normally you'd call it like this:
call_llm(
    prompt="Explain recursion.",
    temperature=0.2,
    max_tokens=500
)


But if you already have all those arguments in a dictionary:
kwargs = {
    "prompt": "Explain recursion.",
    "temperature": 0.2,
    "max_tokens": 500
}
you can use:
call_llm(**kwargs)


Where does generate_params_dict(...) fit?
Suppose your codebase has:

def generate_params_dict(user_question):
    return {
        "prompt": f"Answer this question: {user_question}",
        "temperature": 0.3,
        "max_tokens": 1000
    }

Then another part of the code might do:
kwargs = generate_params_dict("What is recursion?")
response = call_llm(**kwargs)
```

- max_tokens — a hard cap on how long the model's response can be. If you only need one word back ("FAQ" or "Product"), you set this low (e.g. 10) so the model can't ramble and waste money.

- top_p — another randomness control, used alongside temperature. Lower = more focused/safe word choices. Higher = more variety.

- Span / tracing (tracer.start_as_current_span(...)) — this is not about the AI logic at all. It's a logging/monitoring tool. Every with tracer.start_as_current_span("name") as span: block creates a labeled checkpoint that records: what went in, what came out, how many tokens were used, whether it errored. This is what lets you later "trace" a single user question through the whole system to see exactly which step went wrong or cost too much.

