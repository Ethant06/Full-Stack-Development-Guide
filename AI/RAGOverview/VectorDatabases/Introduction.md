# Why Databases in RAG

- We need a database or index to implement retrieval, since retrieval means to search through stored data fast. We can't efficiently search millions of documents on the fly without some sort of database.
- RAG works by retrieving relevant context before generating an answer so we need **Persistent storage** for our document chunks/embeddings since we do not want to re-embed our entire corpus everytie someone asks a question. We need **Fast Retrieval** at query time, as given a user's question we need to find the most relevant pieces of text out of millions in milliseconds. **Scalability** as our corpus grows and lookups need to stay fast.

###### How keyword Search is implemented Relational
Keyword uses an inverted index - basically a lookup table:
```
"flight"   → [doc1, doc5, doc9]
"cheap"    → [doc1, doc3]
"budget"   → [doc3, doc7]
```
- When we query, it looks up the words in it and finds matching docs ranked by scoring algorithm like **BM25 (how rare/important a word is)**
- **Tools that implement Keyword**: ElastiSearch, PostgreSQL full-text search, Apache Lucene, OpenSearch

###### Why Vector DB over relational DB
- Relational databases are built for exact-match, optimized for things like **WHERE user_id == 123**. This works if there is a precise, structured condition.
- RAG retrieval finds the most semantically similar documents to a query and that performs nearest-neighbor search on high-dimensional embeddings, not a match condition. Relational DB have no native way to do this efficiently.

# Nearest Neighbor Search (Optimized by Vector Databases)
ANN works with our classic cosine/Euclidean distance for retrieval.
- We need ANN since if we did brute force K-Nearest Neighbors (strategy/procedure), and computed with cosine similarity between our query vector and every vector in the database then sort:
```
1 query vs 10 million vectors = 10 million distance calculations for every single query
```
- It is O(N) scale so it is sow and does not scale.
- **ANN** is a way to narrow down which vectors are even worth comparing, so we do not go through every single document vector.

# How Vector Search Scales
- KNN scales linearly and is too slow for large-scale production systems.
- ANN is a family of algorthms that use smart data structures to search must faster. Although it sacrifices accuracy and not guaranteed to find the absolute closest match. This is also precomputed before any queries come in (graph building is expensive at the win of a one-time cost)

###### Algorithm 1: Navigable Small World
Setup is done in advance:
1. Calculate distance between every vector and every other vector.
2. Build a proximity graph - one node per document
3. Connect each node to a few of its closest neighboring documents (creates a "web" structure)

Search Process:
1. Start at a random node (candidate vector) - no assumption it's close to the query
2. Look at its neighbors, move to whichever is closest to the query vector
3. Repeat - keep hopping to closer neighbors.
4. Stop when no neighbor is closer than the current candidate -> Return that candidate

###### Algorithm 2: Hierarchical Navigable Small World (HNSW)
Improves on NSW by adding layers:
1. Layer 3: Small random subset (e.g., 10 of 1,000 vectors)
2. Layer 2: Larger subset (e.g., 100 of 1,000 vectors)
3. Layer 1L All vectors (e.g. all 1,000 vectors)

Search Process:

1. Start at top layer (fewest vectors) -> Find best candidate there
2. Drop down to next layer, starting from that candidate -> refine
3. Repeat until we reach the bottom layer (all vectors) -> Final candidate returned
4. Overall, scales to billions of vectors with only milliseconds of latency - log

