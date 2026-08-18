# Search Architectures: Bi-encoder vs cross-encoder vs colbert
This compares three ways to score how relevant a document is to a query.

#### 1. Bi-Encoder (what you've used throughout the course) Primitie as standard architecture.

How it works:

- Documents and prompt are embedded separately, each into a single vector
- Documents can be embedded ahead of time (before any query arrives)
- At query time, only the prompt needs embedding → then ANN search finds close document vectors

Why "bi"-encoder: two separate encoding passes — one for docs (precomputed), one for the prompt (at query time).

Trade-offs:
✅ Fast — most of the work is precomputed
✅ Minimal storage — one vector per document
⚠️ Lower quality — doesn't capture deep interaction between query and document meaning

#### 2. Cross-Encoder (highest quality, but doesn't scale)

- Concatenates prompt + document together as one input, run through the model
- Outputs a single relevancy score (0–1) — essentially "probability this is a good match"
- Because the model sees both texts together, it captures much deeper contextual interaction than a bi-encoder

Example: Query "great places to eat in New York" + Document → concatenated → model outputs score (e.g. 0.7)

Trade-offs:
✅ Best search quality/relevance of the three
❌ Can't precompute anything — you don't have the prompt until the user submits it, so every document must be scored fresh, per query
❌ Scales terribly — millions/billions of documents = billions of prompt-document pairs to score per single query
Verdict: too slow to be a default search method, but excellent as a re-ranker (score a small shortlist after initial retrieval) — this is teased for a later video

#### 3. ColBERT (middle ground — "contextualized late interaction over BERT")

- Like a bi-encoder, documents are embedded ahead of time — but instead of one vector per document, it creates one vector per token. A 1,000-token document → 1,000 vectors.
- Query is also embedded token-by-token
- Scoring (MaxSim): every prompt token compares against every document token → builds a big grid of similarity scores → each prompt token keeps its single best matching - - document token → those max scores are summed into one overall relevancy score

Example: "New" and "York" (prompt tokens) match strongly with "New York" (in the document); "Eat" matches with "Cuisine" — captures nuanced token-level relevance a bi-encoder's single vector would blur together.

Trade-offs:
✅ Quality close to cross-encoder
✅ Speed close to bi-encoder (docs still precomputed)
❌ Massive storage cost — vectors scale with token count, not per-document. A 2,000-token doc needs 2,000 vectors vs. 1 for a bi-encoder — orders of magnitude more storage
Best suited for high-stakes domains (legal, medical) where retrieval precision justifies the storage cost


# Reranking Concept

A post-retrieval step that rescores and reorders documents after the vector database returnd them, but before they're sent to the LLM. This is how you combine the speed of a bi-encoder with the quality of a cross-encoder.

### Why it's needed

Vector search returns documents that are semantically related but not necessarily directly relevant.

Example: Query = "What is the capital of Canada?"

Vector search might return:

"Toronto is in Canada" — related but wrong answer
"The capital of France is Paris" — related concept (capitals) but wrong country
"Canada is the maple syrup capital of the world" — shares the word "capital" but irrelevant

All of these are semantically close to the query vector, but none actually answer it well. Reranking fixes this by applying a smarter, more expensive model to just this shortlist.

### How the pipeline works
```
Step 1: Over-fetch    → Vector DB retrieves a wider net (20–100 documents, typically via hybrid search)
Step 2: Rerank         → A more powerful model re-scores just this shortlist
Step 3: Truncate       → Only the top 5–10 re-ranked documents are kept
Step 4: Send to LLM    → Final, higher-quality context
```

### Two reranking approaches
1. Cross-encoder reranking (most common)
- Same architecture discussed earlier — concatenates prompt + document, outputs a relevance score
- Adds some latency, but small since only re-scoring a handful of documents
- Considered "almost always worth it" — good trade-off of latency vs. quality

2. LLM-based reranking (emerging)
- Similar concept, but an LLM directly evaluates the prompt-document pair and outputs a relevance score instead of a specialized cross-encoder model
- Same fundamental limitation as cross-encoders: can't precompute anything (needs the prompt present), and scoring each document is costly
- Still only viable as a reranking step on an already-narrowed list, not as primary search


# Takeaway
```
Vector search (bi-encoder + ANN)  → fast, cheap, casts a wide net (20-100 candidates)
Reranker (cross-encoder or LLM)   → slow but accurate, refines the wide net down to top 5-10
Result: fast at scale + high final relevance, because expensive scoring only touches a small subset