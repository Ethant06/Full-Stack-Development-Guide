# Why Databases in RAG

- We need a database or index to implement retrieval, since retrieval means to search through stored data fast. We can't efficiently search millions of documents on the fly without some sort of database.
- RAG works by retrieving relevant context before generating an answer so we need **Persistent storage** for our document chunks/embeddings since we do not want to re-embed our entire corpus everytie someone asks a question. We need **Fast Retrieval** at query time, as given a user's question we need to find the most relevant pieces of text out of millions in milliseconds. **Scalability** as our corpus grows and lookups need to stay fast.

###### How keyword Search is implemented
Keyword uses an inverted index - basically a lookup table:
```
"flight"   → [doc1, doc5, doc9]
"cheap"    → [doc1, doc3]
"budget"   → [doc3, doc7]
```
