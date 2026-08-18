# pgvector Walkthrough

Companion to `Notebooks/pgvector.ipynb`. This is the retrieval half of RAG in miniature: embed documents, store them in Postgres, embed a question, return the nearest rows.

## What we built

A tiny semantic search over 8 sentences in PostgreSQL using the `pgvector` extension. No FastAPI, no chunking, no LLM answer — just **store vectors** and **query by distance**.

## Setup (outside the notebook)

Postgres needs the vector type before Python can insert embeddings:

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE items (
  id SERIAL PRIMARY KEY,
  content TEXT,
  embedding vector(1536)
);
```

`1536` matches OpenAI's default embedding size (`text-embedding-ada-002` via `OpenAIEmbeddings()`).

The notebook connects as:

```
dbname=vectortutorialdb user=postgres password=postgres
```

## Step 1 — Embed the documents

We took 8 short texts (Python, Postgres, vector DBs, RAG, FastAPI, NumPy, PyTorch, Git) and ran each through OpenAI:

```python
embeddings = OpenAIEmbeddings()  # reads OPENAI_API_KEY
embeddings_list.append(embeddings.embed_query(text))
```

- Text in → list of 1536 floats out.
- We embed **once** and store the result. We do not re-embed the corpus on every question.

## Step 2 — Insert into Postgres

```python
cursor.execute(
  "INSERT INTO items (content, embedding) VALUES (%s, %s)",
  (content, embedding),
)
```

Each row is the original sentence plus its vector. `psycopg2` sends the Python list; pgvector stores it as `vector(1536)`.

## Step 3 — Embed the query and search

Question used:

> How can I give an AI model relevant information from a collection of stored documents?

That sentence is embedded the **same way** as the documents, then ranked with pgvector's distance operator:

```sql
SELECT id, content
FROM items
ORDER BY embedding <-> %s::vector
LIMIT 3
```

- `<->` is **L2 (Euclidean) distance**. Smaller = closer = more similar.
- `::vector` casts the query list so Postgres treats it as a vector, not a generic array.
- `LIMIT 3` is top-k retrieval.

## Why pgvector here

Vectors live in the same Postgres we already use for the rest of the app. Fine for learning and small scale. Dedicated vector DBs (Pinecone, Weaviate, etc.) matter more when you need ANN indexes, hybrid search, or many millions of vectors. See `Workflow.md`.
