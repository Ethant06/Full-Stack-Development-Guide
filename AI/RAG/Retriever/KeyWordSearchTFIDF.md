# KeyWord Search


#### Say our RAG system has 3 documents

Document 1:
```
I love making pizza at home. You can make pizza without a pizza oven.
```

Document 2:
```
Ovens are useful for baking bread, cookies, and cakes.
```

Document 3:
```
Making pasta at home is easy. You only need flour, eggs, and water.
```

#### User query

Now the user asks: **"How can I make pizza without an oven?"**

## Step 1. Turn word into Numbers TERM FREQUENCY (TF)

Computer need numerical representations so imagine our vocab is:

```
I
love
making
pizza
without
oven
pasta
flour
eggs
```
We can represent a document as a vector. For example:
```
"making pizza pizza"

[0, 0, 1, 2, 0, 0, 0, 0, 0]
```
- The numbers represent how many times each word occurs. This is the **TF**
- This is called a sparse vector since the vocab might contain 50,000 words but our document might only contain 500.
- Hence most of the vector is going to be zero

# Step 2. Inverted Index
- Say we have 1 million documents. We dont want to scan every document every time someone searches for **pizza oven".
- Instead, we create an index ahead of time:
```
pizza  → Document 1, Document 7, Document 43, Document 891...
oven   → Document 1, Document 2, Document 55...
pasta  → Document 3, Document 17, Document 900...
```
So rather than asking each document what word it contains, we can ask word -> which documents contain it? (Inverted)
- This is essential since when the user searches **pizza oven**, the search engine can imediately find
```
pizza → documents containing pizza
oven  → documents containing oven
```

# Simplest scoring system
Suppose our query is **pizza oven**
```
Document	 pizza?	oven?
D1	         ✓	   ✓
D2	         ✗	   ✓
D3	         ✗	   ✗
```
so we could simply give:
```
D1 = 2
D2 = 1
D3 = 0
```
So D1 ranks the highest. However, there are problems.

## Problem 1. What if the word appears multiple times?

D1:
```
Pizza is great. I love pizza. Pizza is my favorite food.
```

D2:
```
I like pizza
```
Both contain "pizza" but D1 talks about it much more.
- Hence we use
```
TF(pizza, D1) = 3
TF(pizza, D2) = 1
```
This is the term frequency (TF). The more frequently a term occurs in a document, the more strongly that document may be about that term.

###### Additional Problem to TF

1. Document A - words: 100 pizza: 5
2. Document B - words: 10,000 pizza: 20
- We simply count term frequency, we would rank 5 higher but that would be misleading since pizza represents 5/100 of Doc A but only 20/10,000 of Doc B, so A actually has more focus on pizza.
- Our solution is to normalize term frequency by document length:
```
A → 5 / 100 = 0.05
B → 20 / 10,000 = 0.002
```
Now A gets a higher score

## Problem 2: Redundancy
- Consider Query A: "the pizza" and Query B: "pizza oven"
- Suppose the document contains "the the the the the the pizza"
- If we now simply count the matching words, "the" contributes just as much as "pizza" but "the" does not tell us much about relevance. It appears in practically every English document. But Pizza might only appear in only 1% of the documents. So Pizza is much more informative.
###### Solution is IDF
This asks **How useful is this word for distinguishing documents from one another?**
- Say 100 documents and the word **The** appears in 100/100 documents, so it's common.
- Word **Pizza** appears in 5/100 documents, much rarer.
- Word *Quantum** appears in 1/100 Documents, even rarer.
So Ideally we want:
```
the      → low importance
pizza    → higher importance
quantum  → very high importance
```
This is what **IDF** captures
```
IDF(t) = log(N/df(t))

- N = total # of documents
- df(t) = number of documents containing the term t
```

```
IDF(the) = log(100/100) = 0 - not much importance
IDF(pizza) = log(100/5) = log(20) - significantly larger value
IDF(quantum) = log(100/1) = log(100) - largest
```
The main principle is the **more documents a word appears in, the less useful it is for identifying relevant documents.
- Rare word = high IDF and common word = low IDF

# Step 3. Combine TF and IDF

We have two pieces of information:
- TF: How important this word is within this particular document. Does this document talk about this word a lot?
- IDF: How useful/informative this word across the entire collection of documents. Is this word unusual across the entire collection? Is this useful for distinguishing relevant documents?
```
**TFIDF = TF * IDF**
```

# Step 4. Scoring Documents
High TF-IDF: Word appears frequently but is extremely common
Low TF-IDF: The word is rare but only appears once

###### What happens now when the query comes in?
This is the entire retrieval process.
1. Analyze documents- find words and their frequencies.
2. Calculate IDF.
3. Build the index and store information that allows system to quickly find documents containing each word.
4. Now the knowledge base is ready