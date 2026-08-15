# Origin Transformers - a specific neural network design
Transformer architecture (2017, "Attention is all you need") had two parts:
1. an encoder (builds deep understanding of input text)
2. Decoder (generates new text from that understanding) - is a neural network
- LLMS = decoder only, as they just generate text
- Embedding models = encoder only as they build semantic representations, which power our vector search.

# LLM Process Decoder

###### 1. Tokenization
Prompt is split into tokens

###### 2. Initial embeddings
Each token gets:
- A first-guess dense vector (its raw, static meaning — same every time regardless of context)
- A positional vector (where it sits in the sequence)

###### 3. Attention Mechanism - neural network
Every token looks at every other token and decides how much to "attend to" each one — i.e., which other tokens should shape its meaning.

Example: In "the brown dog sat next to the red fox" — "dog" pays most attention to "brown" and "sat," since those relate directly to it.

Uses multiple attention heads in parallel — each specializes in different relationship types (e.g., one head tracks object-descriptor pairs, another tracks spatial relationships)
Small models: ~8–16 heads; large models: 100+
These relationships aren't human-designed — they're learned automatically during training

###### 4. Feedforward phase - neural network doing their traditional jobs: transforming a vector representation into a new refined vector representation.
The largest part of the model (most parameters live here)
Takes each token's embedding + position + attention info and produces an updated ("second-guess") vector for that token, now context-informed


###### 5. Repeat (multiple layers)

This attention → feedforward cycle repeats 8–64 times, refining each token's meaning progressively (guess → better guess → even better guess...).

###### 6. Generation
Model computes a probability distribution over its entire vocabulary (even 100,000+ tokens, most near-zero probability) for "what comes next"
Picks one token, weighted by probability (likely tokens chosen more often, but any token has a nonzero chance)
Appends that token, then repeats the entire process (decoder pass) for the next token — meaning early token choices influence everything generated afterward
Stops at a token limit or when it generates an end-of-completion token
Final tokens are de-tokenized back into readable text

# Overall
```
"Neural network" = the general concept: learned weights transforming vectors
"Transformer"     = a specific, powerful neural network architecture/blueprint
"Decoder"         = the transformer component LLMs use (built from attention + feedforward NN layers)
"ChatGPT"         = a decoder-only transformer — so yes, fundamentally, still "a neural network,"
                    just a very large, specifically-structured one
```
```
Tokenize → embed (first guess) → add position →
Attention (who matters to whom) → Feedforward (refine meaning) → repeat 8-64x →
Predict next token probability → sample one → repeat for each new token
```