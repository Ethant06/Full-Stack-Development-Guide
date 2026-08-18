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

# Fine Tuning

#### RAG retrieves information from your database and puts it into the prompt.
```
User question
     ↓
Retrieve information
     ↓
Add information to prompt
     ↓
LLM
     ↓
Answer
```
Best for:
```
New/current information
Company documents
Product catalogs
Policies
Knowledge bases
Information that changes frequently
```

#### Fine Tuning changes the model's internal parameters by training it on your examples.
```
Training examples
      ↓
Fine-tune model
      ↓
Specialized model
      ↓
New questions
      ↓
Specialized answers
```

Best for:
```
Specialized behavior
Consistent style
Specific formats
Domain adaptation
Specialized tasks
```
# Example
Suppose your a building a customer-service chatbot.

```
You want it to know:

"Our return policy is 30 days."

Use RAG because this information may change.

You want it to always answer:

"Respond in a friendly, concise customer-service style."

Fine-tuning could help with that behavior.
```
- They can however work together/complementary tools
