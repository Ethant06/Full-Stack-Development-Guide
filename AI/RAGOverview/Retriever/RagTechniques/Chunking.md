# Chunking Key Concepts
Breaking long documents into smaller text pieces before embedding them, instead of vectorizing whole documents.

# Significance
1. Embedding models have input length limits
2. Improves search relevancy (smaller, focused chuncks -> sharper vectors). If we embedded a whole book into a single vector, these vectors would not be able to give sharp representation of any specific topic/concept discussed in a particular chapter or page, and instead kind of averages across all of them.
3. Keeps LLM conext window from filling up with irrelevant text. LLM typically have limitations on the amount of text they can process at once (Context Window)
4. Too small however loses surrounding context and hurts relevance as well. We ideally need a balance.

# Chunking Strategies
1. fixed-size chunking:
- split every N characters (250 chars per chunk)
- However can land mid-word or mid-thought

2. Fixed size with overlap
- Chunks overlap by a %(e.g., 10%) with neighbors
- reduces context loss at chunk boundaries
- Trade-off is more redundant vectors stored -> more storage

3. Recursive character text splitting or Variable-Size chunking
- Spit on meaningful character such as newline for paragraphs.


# Advanced Chunking Techniques

###### Semantic Chunking
Places sentences together in chunks if they have similar meaning.
- For each sentence, it decides if it's similar enough to the previous sentences, and so belongs in the same chunk, or is different.
- To do this, both the contents of the current chunk and the following sentence are vectorized. If the two vector are below some threshold distance away from each other, they have similar meanings, and the sentences are added to the samw chunk. This continues until eventually the growing chunk is too different from the following sentence. At this point, you cut off the chunk and restart the whole process from that next sentence.
- Pros: Higher recall and precision.
- Cons: Chunking can be computationally expensive. Requires repeated vector calculations.

###### Language based chunking.
- Prompt LLM to create chunks from a document. Include instructions on types of chunks like keeping concepts together. This is high performing and model cost decreases.

###### Improement for any chunking strategy. This works and applies in every chunking strategy.
- Use a language model to add context to every chunk
- For instance, we can ask the language model to create chunks from a document, but also add summary text to the chunk explaining its context in the broader document.
- This required computationally expensive preprocessing, since llm needs to go through your entire knowledge base one document and chunk at a time to add context.