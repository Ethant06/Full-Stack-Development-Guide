# Hybrid Search Pipeline.

1. A prompt is received by the retriever.
2. The retriever then performs both a keyword search and a semantic search using that prompt. This results in two ranked lists of documents, one that was scored and ranked using keyword search and another using semantic search.
3. Then a metadata filter is applied to both lists to remove irrelevant douments.
4. These two ranked lists need to e cobined to form a single ranking. Done by **Reciprocal Rank Fusion**

# Reciprocal Rank Fusion
- Rewards documents for being highly ranked in each list
- Control weight of keyword vs semantic ranking.
```
1 / (k + rank in list 1) + 1 / (k + rank in list 2) + ... + 1 / (k + rank in list n)
where k is a hyperparameter
```
For each document. Then total points from all ranked list used to perform final ranking.
For example:

```
A document scores 2nd in Keyword Rank and 10th in Semantic rank
1/2 + 1/10 = 0.5 + 0.1 = 0.6 total score
```
This score reranks all the documents.

# Beta: Weighting semantic vs. keyword
- Beta is a hyperparameter and say B = 0.8
- This means semantic search has 80% importance and only 20% to ranking provided by keyword search.
- This hyperparameter depends on the goal of our retriever and RAG system.


# Important Decision Makings
There are many decisions that come with a hybrid system.

- Adjusting parameters of BM25 algorithm
- Choosing which metadata to filter on
- Changing the weighting of keyword versus semantic search in the reciprocal rank fusion.
This system lets us leverage each approach's strengths and tune the syste's performance to the data in our knowledge base or goal of overall project.
**To tune however we need a way to measure how well a retriever is performing.**
