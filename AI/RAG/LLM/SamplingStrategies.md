# Controlling Randomness
Every token an llm generates is a weighted random choice from a probability distribution over its entire vocabulary. Controlling how that choice is made is how we tune LLM behavior.


## Greedy Decoding
Always pick the single highest-probability token — no randomness at all
✅ Deterministic — same prompt always produces same output
❌ Can feel generic/predictable, and the model can get stuck in repetitive loops with no way to break out (it doesn't care if the overall output makes sense, just picks the top token each step)
Good for: code completion, debugging — anywhere pure predictability is desired

## Temperature (the main control knob)

Reshapes the probability distribution curve — doesn't reorder token likelihoods, just changes how spiky/flat the distribution is.

Temperature	Effect
```
0	= greedy decoding (top token gets 100% probability)
1 (default)	Original, unmodified distribution
1.1–1.3	Flatter distribution → more variety, more creative output
Too high	Nearly flat — all tokens roughly equal chance, risk of nonsense
```

## Sampling techniques (to cut off the "long tail" of nonsense tokens)
##### Top-k sampling
Restrict choices to the k most likely tokens (e.g., top 5)
Fixed pool size regardless of how confident/uncertain the model is

##### Top-p sampling (nucleus sampling)
Restrict choices to the smallest set of tokens whose cumulative probability crosses a threshold (e.g., 85%)
More dynamic than top-k: if the model is confident (few tokens dominate), the pool shrinks naturally; if uncertain (flat distribution), the pool expands to include more options

## Word-level controls
##### Repetition penalty
Reduces probability of tokens/words already used in the completion → less repetitive, more natural-sounding text

##### Logit biasing
Manually boost or suppress probability of specific tokens, permanently
Use cases: bias down profanity in a RAG system; bias up specific category labels if your LLM is acting as a classifier


# Standard starting config:
```
temperature = 0.8
top_p = 0.9
repetition_penalty = 1.2
```
- Factual/code tasks → lower temperature + lower top-p (more conservative, deterministic). Great for producing code that is deterministic and have known answer.
- Creative tasks → higher temperature + higher top-p (more exploratory, varied)
- Add repetition penalties / logit biasing after identifying specific issues in your outputs, not by default