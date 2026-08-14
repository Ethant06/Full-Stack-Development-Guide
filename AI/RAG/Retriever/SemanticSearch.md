# High Level

- Prompt and documents each get a vector. Then each vectors are compared to generate scores. The difference between semantic and keyword is we generate vectors by running document/prompt through special mathematical model called an embedding model.
- Embedding model map words to a location in space and this location is represented by a vector. The cool thing is embedding models will map similar words in similar vector space (e.g., food and cuisine close to each other).
- More dimensional space means more room to form clusters and capture nuanced relationships.

# High Level Functionality Semantic Search
- All documents are projected onto the vector space through the embedding model. Documents with similar meaning with be closer to each other.
- We also embed the prompt so that it gets a vector of its own. Then the similarity between this prompt's vector and other vectors in the database can be calculated. These vector embeddings capture nuances in a way that no other search technique provides.
- Then we can rank documents by distance so whichever documents are closest to the prompt will be returned.

# Ways to calculate similarity

After converting prompts and documents into vectors, we check their similarity using distance measures.

##### 1. Cosine Similarity
This evaluates how close two vectors are based on their angle.

```
A⋅B=∥A∥∥B∥cos(θ) and the cosine similarity is cos(0) - Basically length of A * length of B's shadow onto A. |B|Cos(0) is basically the mount of B vector pointing near same direction as A
If they point in the same direction the angle is small 0 = 0 degrees and cos(0) = 1
```
- The closer cosine is to 1, the more similar.
- If they are perpendicular, then 0 = 90 degrees and cos(90) = 0, so closer to 0 -> unrelated directions
- If they are opposite directions 0 = 180 degrees, then cos(180) = -1 so cos close to -1 means opposite.
- Now why not just use dot product? Two dot products A and C might point in the same direction, but one can be significantly larger. Cosine similarity removes the effect of magnitude COS(A, C) = 1 because they point in the same direction.

##### 2. Euclidean Distance
This calculates the straight-line distance between two vectors in the embedding space. So how far apart these vectors are.

```
d(A, B) = sqrt[summation n (a_i - b_i) ** 2].
So d((2,3), (5,7)) = 5
```
The lower the closer.

# Framework
1. Create the embedding: use embedding model to convert query and documents into vectors. Svae this so we can load pre-computed embeddings. We don't want to run the embedding model over all our documents everytime a user searches.
2. Metric measurement: Use similarity metric to determine closeness of each document to our query.
3. Soting: Sort documents by their similarity score and select top most relevant.