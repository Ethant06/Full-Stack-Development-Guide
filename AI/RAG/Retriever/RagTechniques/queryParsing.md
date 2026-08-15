# Problem

Human-written prompts (conversational, messy) makes bad search queries for vector retrieval. It is not recommended to feed raw user prompts directly into the retriever. Solution is to parse/transform the prompt before it hits the database.

#### 1. Query Rewriting (standard and most used)
- Use LLM to rewrite the user's raw prompt into a cleaner searh query.
- Typical instructions: clarify ambiguous phrase, add domain terminology, strip irrelevant details.
Example (medical RAG):
```
Raw: "I was walking my dog... she yanked the leash... my shoulder is numb, fingers are pins and needles..."
Rewritten: "Sudden forceful pull on shoulder resulting in persistent shoulder and finger numbness for three days. Potential causes such as neuropathy or nerve impingement?"
```

#### Named entity recognition - advanced technique
Identifies categories in the query: people, places, dates, characters, etc.
Example model: Gliner — give it text + a list of entity types to detect, it labels matches
Extracted entities can feed into vector search or metadata filtering
Fast/efficient model, adds minor latency, but can meaningfully boost retrieval quality

#### Hypothetical Document embeddings
Instead of embedding the user's question directly, an LLM first generates a hypothetical ideal answer document
That hypothetical document gets embedded, and its vector is used for the search — not the original query's vector
Why it works: normally you're comparing a question against documents (different "shapes" of text — "apples to oranges"). HyDE instead compares a hypothetical document against real documents — more similar text types, better matching
Trade-off: added latency + compute cost (extra LLM call to generate the hypothetical doc)