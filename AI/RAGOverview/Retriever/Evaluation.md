# What we need to evaluate a retriever
1. The prompt
2. The retriever's ranked results: Example [D7, D2, D15, D4]
3. Ground Truth: The documents that we know are actually relevant: {D2, D7, D20}
4. Then we compare the retriever's result agaisnt the ground truth.

# Precision: Of the documents we retrieved, how many were actually relevant? How trustworthy is it.
Measures how many of the returned documents are relevant: Relevant Retrieved / Total Retrieved

# Recall: Of all the relevant documents that exist, how many did we find successfully. How comprehensive is it.
Relevant Retrieved / Total Relevant

# Recall Precision Tradeoffs
The more documents we retrieve, the more likely we are to find all the relevant documents, but we also bring in more irrelevant documents. Higher Recall, but lower Precision.

# Precision@K and Recall@K and Why K Matters

Retrievers usually do not return every document, rather they return the top K.
- Why K matter in RAG? Suppose our retriever returns top 3 documents. We would have very little context going into the LLM.
- But if we returned top 50 dcuments, we might find more relevant information, but we also give the LLM a lot of irrelevant material.
- Hence we need to decide **How many chunks should our retriever return to the LLM"?

We would evaluate different choices for this matter:
```
Recall@3
Recall@5
Recall@10
Precision@3
Precision@5
Precision@10
```
Then we often calculate those and report average.

# Average Precision / Map
Precision and recall do not fully consider where relevant documents appear in the ranking.
For instance:
```
Retriever A
1. ✓
2. x
3. ✗
4. ✗
5. ✗

Retriever B
1. ✗
2. ✗
3. ✗
4. ✗
5. ✓
```
Here Retriever A is better since it puts the relevant document at the top. But both retrieved one relevant document.
###### Average Precision comes in and asks how good the precision is at the positions where we actually found relevant documents. It rewards putting relevant documents early in the ranking.

###### Mean Average Precision (MAP) means calculate AP for many queries and take the average of those AP.

# Reciprocal Rank / MRR
Mrr is mre focused on the first relevant result. It asks how far down the list we have to go before we fnd the first relevant document.

```
**Reciprocal Rank (RR) = 1 / rank of first relevant document**
```
Example:
```
First relevant result	Reciprocal Rank
#1	1.0
#2	0.5
#3	0.33
#5	0.20
#10	0.10
```
So if our first relevant document is at rank #1, then it is good. If it is at #10, then it is bad.
** Mean Reciprocal Rank** = average reciprocal rank across many queries.

# The overall picture
```
                    RAG Retriever
                         │
                         ▼
                    User Query
                         │
                         ▼
                 Retrieve Documents
                         │
                         ▼
                Ranked Top-K Results
                         │
              ┌──────────┴──────────┐
              │                     │
       Ground Truth            Retrieved
       Relevant Docs              Docs
              │                     │
              └──────────┬──────────┘
                         ▼
                  Evaluation Metrics
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      Precision        Recall          MAP/MRR
```
For RAG systems, k=5 to k=20 is often optimal for the recall/precision tradeoff. Recall will always remain relatively low.
#### Recall is usually the most fundamental metric since the first job of a retriever is find the relevant information.
#### Precision just tells us if we are retrieving too much irrelevant information.
#### MAP / MRR tell us how well we rank the relevant information toward the top

