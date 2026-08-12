# Problem Statement
A retriever's job at high level sounds simple, all it does is find documents in the knowledge base that can help an LLM respond to a prompt, however, this is very difficult.
- The documents in our knowledge base might range from personal emails to internal company memos or articles from a medical journal. They are rich and are typically structured in a way for humans to read, but not for computer to search through it.
- Retriever has to work around all of this messy structured information and radpily return the most relevant pieces in seconds.


# Retriever Functionality High Level Process

- It first process the prompt to understand the underlying meaning.
- It uses the meaning to search the index of documents.
- The retriever then returns the documents from the knowledge base that are the most relevant to the prompt.
- Then the retriver ranks documents in the knowledge base by how relevant they are to the prompt.
- Each document receives a numerical score that quantifies its relevance and typically is determined by the similarity between the text of the promt and the text of the document. There are a variety of approaches to calculating the similarity scores.
- The documents are added to an augmented prompt.
- LLMs ground their responses in the retrieved information, so they build their answers using the documents rather than guessing based on its internal memory.

# Nuances

- A well-designed retriever should not only return relevant documents, but also needs to withhold irrelevant documents. If we asked for information and the retriever responded with all the documents in the knowledge base, we'd technically have every relevant document, but it would be lost in a pile of irrelevant information, and this would lead to costly prompts or use up LLM's context window entirely.
- We try our best to perfetly rank and choose the documents. This means we will need to optimize retriever's performance and monitor it over time and experiment with different settings.

# techniques
There are two main search techniques. In often times both follow an extra metadata filter on the documents returned from the searches.

#### Keyword Search
Looks for documents containing the exact words found in the user prompt. Ensures sensitivity to exact words the user included in the prompt.

#### Semantic Search
Looks for documents with similar meaning to the prompt. Semantic search gives more flexibility to find documents whose meaning is similar even without matching words.

#### Metaadata filtering
Excludes documents based on rigid critera and documents metadata like title, author, creation date, access privileges.