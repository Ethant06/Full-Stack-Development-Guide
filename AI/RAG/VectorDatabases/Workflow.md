1. Create/connect to a database instance
2. Create a collection (like a table) — define data fields + which embedding model/vectorizer to use
3. Load data — insert documents (e.g. via batch add), which:
4. Creates sparse vectors → powers keyword search
5. Creates dense embeddings → powers semantic search
6. Build the index (e.g. HNSW) → powers ANN search
7. Run queries

# Pinecone
Most popular and managed for vector databases
It is proprietary and cloud-only
You want zero infrastructure management — fully managed, just an API
You're prototyping fast and don't want to think about hosting
Budget isn't the tightest constraint (~$100-500/month is fine for typical RAG scale)
You don't need self-hosting flexibility (Pinecone is cloud-only, proprietary)

# pgvector (Open Source)
You're already using PostgreSQL (e.g. via Supabase, Neon, or your own setup)
Your scale is under ~5M vectors
You want the fastest path from zero to production — operational simplicity of keeping vectors in your existing database is worth more than a latency edge from a separate system
This is often the pragmatic pick for a first AI feature or learning project

# Weaviate
This is strong for hybrid search use cases