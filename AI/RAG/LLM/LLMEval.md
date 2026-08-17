# 1. Separate Retriever vs. LLM
In a RAG system:
Retriever: Finds relevant information.
LLM: Uses that information to produce the answer.

So if the retrieved documents are bad, changing the LLM prompt probably won't fix the real problem.

# 2. RAGAS
RAGAS is an open-source framework for evaluating RAG systems.

It provides metrics such as:
```
Response Relevancy → Did I answer the question?
Faithfulness      → Did I use the retrieved information correctly?
Citation quality  → Are my sources actually supporting the answer?
- Many of these evaluations use another LLM as a judge.
```

# 3. A/B testing
This is useful when changing:

System prompt
Temperature
LLM model
Retrieval settings
Other configuration
You compare the old vs. new version and measure the impact.
