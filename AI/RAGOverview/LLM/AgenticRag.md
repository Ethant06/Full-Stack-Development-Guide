Rather than using one LLM to do everything, we use multiple LLMs with each one responsible for a specific task.

# Normal Rag
```
User
 ↓
Retriever
 ↓
One LLM
 ↓
Answer
```

# Agentic Rag
```
User
 ↓
Router LLM
 ↓
Should we retrieve?
 ↓
Retriever
 ↓
Evaluator LLM
 ↓
Enough information?
 ↓
Answer LLM
 ↓
Citation LLM
 ↓
Final answer
```

# Example: User asks: What is your return policy for shoes?

#### Step 1 — Router
A small, cheap LLM decides:
```
Does this question require retrieval?
→ YES
```

#### Step 2 — Retriever
Searches the vector database and finds relevant documents.

#### Step 3 — Evaluator
Another LLM checks:
```
Are these documents sufficient?
→ NO
```
So the system retrieves more information.

Then:
```
Are the documents sufficient?
→ YES
```

#### Step 4 — Answer LLM
Uses the retrieved information to generate the answer.

#### Step 5 — Citation LLM
Adds/validates citations.

# 4 Common Agentic Workflows

#### 1. Sequential
Everything happens in order:
```
Query Parser
 ↓
Query Rewriter
 ↓
Retriever
 ↓
Answer Generator
 ↓
Citation Generator

Each model handles one step.
```

#### 2. Conditional
An LLM decides which path to take.
```

                ┌→ Answer directly
User → Router ──┤
                └→ Retrieve → Answer
```
Useful when some questions don't need RAG.

#### 3. Iterative
The system can loop and try again.
```
Generate answer
      ↓
Evaluate
      ↓
Good? ── YES → Done
  │
  NO
  ↓
Try again
```
Useful for things like code generation or complex research.

#### 4. Parallel
Multiple LLMs work on different parts at the same time.
```
             ┌→ LLM → Analyze Paper A ─┐
User → Split ┤                          ├→ Synthesizer → Answer
             └→ LLM → Analyze Paper B ─┘
```
Useful when you need to analyze multiple independent sources.


# Agentic tools
An agent can have access to tools such as:
```
🔎 Search tool → search a database or website
🗄️ Database tool → query SQL/database
🧮 Calculator/code interpreter → perform calculations
🌐 API tool → interact with an external service
📁 File tool → read or modify files
📚 Vector database → retrieve relevant documents
```

**Why is this called "agentic"?**
Because the system isn't just: Prompt → Answer
Instead, it can: Understand → Decide → Use a tool → Observe result → Decide what to do next → Answer