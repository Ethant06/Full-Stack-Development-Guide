Modern search systems often use BM25, which improves upon the basic TF-IDF approach.

You can think of the progression as:

Basic keyword matching
        ↓
Term frequency
        ↓
Normalized term frequency
        ↓
TF-IDF
        ↓
BM25

BM25 handles things like:

- term frequency saturation
- document length normalization
- how often a term occurs across documents
all better than basic TF-IDF.