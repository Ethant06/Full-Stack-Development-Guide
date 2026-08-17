Observability is knowing how well your RAG system is workig and why

# Performance
```
Latency
Throughput
Memory/compute usage
Tokens/second
```

# Quality
```
User satisfaction
Retriever precision/recall
Response relevance
Faithfulness
Citation quality
```

# Scope
System-level — high-level overview of overall performance
Component-level — isolates which piece (retriever, LLM, etc.) is causing a problem
```
When changing:
LLM
Prompt
Retriever
Model settings
Use A/B testing or controlled experiments to see whether quality actually improves.
```

# Three types of evaluators
```
Code-based — cheapest, deterministic, automatic (e.g., request counts, JSON validity checks)
Human feedback — most informative but costly (e.g., thumbs up/down, annotated test sets for precision/recall)
LLM-as-judge — a middle ground; more flexible than code, cheaper than humans (e.g., grading retrieval relevance). Requires careful tuning — models can be biased toward outputs from their own family, and work best with discrete labels (relevant/irrelevant) rather than numeric scales.
```

# Recommended starting setup
Use code-based evals for performance metrics (latency, throughput, tokens/sec) at both component and system level — cheap and easy
Use human feedback (thumbs up/down) for system-wide response quality
Use human-annotated test sets to calculate retriever precision/recall
Use LLM-as-judge (e.g., via Ragas) to assess LLM output quality — relevancy, citation quality, ability to ignore irrelevant context



# Logging, monitoring, and observability
Why use an observability platform: Purpose-built tools handle common evaluation tasks (metrics, logging, experimentation) so you spend less time building infrastructure and more time monitoring/improving your system.

# Example platform: Phoenix (by Arise) — open-source observability/eval platform, with key features:

- 1. Traces — the most commonly used tool
Follows a single prompt's full path through the RAG pipeline: initial prompt → retriever query → retrieved chunks → re-ranker output → final LLM prompt → generated response
      - Records step-level latency
      - Useful for both prototyping and production; especially valuable for diagnosing why a specific prompt performed poorly
- 2. Eval integrations — integrates with libraries like RAGAS, making it easy to calculate metrics such as retriever search relevancy or citation accuracy
- 3. Experimentation — supports iterative prompt testing and A/B testing to measure whether changes (new system prompts, adding a re-ranker, etc.) actually improve performance
- 4. Aggregate reporting — provides daily high-level reports (e.g., retriever accuracy, model hallucination rate) alongside the low-level trace data

Limitations: Platforms like Phoenix don't cover everything — e.g., they're not well-suited for monitoring vector database compute/memory usage. For those gaps, use traditional infrastructure monitoring tools like Datadog or Grafan