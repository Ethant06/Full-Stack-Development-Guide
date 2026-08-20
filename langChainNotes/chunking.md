```
def split_documents(documents, chunk_size = 600, chunk_overlap=200):
  text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = chunk_size,
    chunk_overlap=chunk_overlap,
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
  )
```
- chunk_size=600 - target max size of each chunk which here is 600
- chunk_overlap=200 - each chunk repeats the last 200 characters of the previous chunk. This is so that sentences that gets cut at a chunk boundary still has context in the next chunk (important for retrieval)
- separators = ["\n\n", "\n", " ", ""] - the recursive part where it tries to split on the first separator in the list:
```
Try splitting on "\n\n" (paragraph breaks) first — keeps whole paragraphs together if possible.
If a resulting piece is still bigger than chunk_size, split that piece on "\n" (line breaks).
If still too big, split on " " (words) — avoids breaking mid-word.
If still too big, split on "" (individual characters) — last resort, brute-force cut.
```