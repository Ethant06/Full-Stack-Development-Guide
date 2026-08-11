# Retriever Functionality

- It first process the prompt to understand the underlying meaning.
- It uses the meaning to search the index of documents.
- The retriever then returns the documents from the knowledge base that are the most relevant to the prompt.
- Then the retriver ranks documents in the knowledge base by how relevant they are to the prompt.
- Each document receives a numerical score that quantifies its relevance and typically is determined by the similarity between the text of the promt and the text of the document. There are a variety of approaches to calculating the similarity scores.

# Nuances

- A well-designed retriever should not only return relevant documents, but also needs to withhold irrelevant documents. If we asked for information and the retriever responded with all the documents in the knowledge base, we'd technically have every relevant document, but it would be lost in a pile of irrelevant information, and this would lead to costly prompts or use up LLM's context window entirely.
- We try our best to perfetly rank and choose the documents. This means we will need to optimize retriever's performance and monitor it over time and experiment with different settings.