# 1. What is prompt engineering?
Designing instructions and context so an LLM produces better answers.

- For RAG, a good prompt usually comines Instructions + conversation + retrieved documents + user question

# 2. Messages Format
LLMs commonly receive prompts as a list of messages. Each message has:
```
{
  "role": "system",
  "content": "Your instructions here."
}
```
```
Role	  Purpose
system	Controls the LLM's overall behavior. The systems message gives high-level instruction that applys to LLM's behavior.
user	Contains the user's question/input. In RAG we also add retrieved context before question.
assistant	Contains previous LLM responses
- The llm does not actually remember the previous conversation. Instead our application sends the relevant conversation again with the new request.
```

# Prompt Templates RAG with retrieval
```
[
  {
    "role": "system",
    "content": "You are a helpful RAG assistant. Answer using only the retrieved context. Do not make up information. If the answer is not present, say you don't know. Respond in concise Markdown."
  },
  {
    "role": "user",
    "content": "What are the benefits of RAG?"
  },
  {
    "role": "assistant",
    "content": "RAG can provide answers using external information rather than relying only on the model's training data."
  },
  {
    "role": "user",
    "content": "Retrieved context:\n\nDocument 1:\nRAG allows language models to retrieve relevant information from external sources.\n\nDocument 2:\nRAG can improve factual accuracy by grounding responses in retrieved information.\n\nQuestion:\nWhat are the benefits of RAG?"
  }
]
``
# Overall Architecture
```
User asks question
        ↓
Retriever searches database
        ↓
Top relevant chunks
        ↓
Prompt Template
        ↓
System instructions
+ Conversation history
+ Retrieved context
+ User question
        ↓
LLM
        ↓
Final answer
```