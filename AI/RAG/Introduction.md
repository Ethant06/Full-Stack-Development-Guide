# What is RAG

Retrieval Augmented Generation is the most widely used technique for improving quality and accuracy of a LLM's response. A model starts off knowing only information from the public internet data it was trained on, so if we needed to answer questions from a proprietary data, such as our own documents - RAG lets the mdodel do this by providing the model access to that additional data. This lets an LLM answer questions with facts that it was not already trained on - ensuring the response is up-to-date and accurate.

# Agentic RAG

- Systems that use multiple large language models where each one handles a single part of a large workflow and has the agency to decide what data to retrieve.
- Earlier generation of RAG was a human engineer writing rules to decide how to take a long document or proprietary data, how to cut it into pieces, how to retrieve it, and then take specific pieces to put into the LLM - **all about human engineer deciding what to give as a context for the LLM to answer the question.** Then it can do deeper as letting the AI agents decide does it want to do a web search next, and if so what keywords does it want to use. Or query a specific specialized database. Or after retrieving the first round of information is it good enough? Should it do another round of retrieval? So these AI agents can decide by themselves what information to retrieve to serve a specific information need.

# LLM BottleNecks

- When prompting an LLM, it relies on general knowledge from reading huge chunks of the internet. It uses this to generate a response and while it works great for many prompts, in some cases the LLM doesn't know the information it needs to respond accurately.
- An LLM often times don't obtain all information. Lots of information won't be included since companies keep private databases and some information is just hidden or hard to access. And with news being published every day, there will always be information out there that an LLM was not trained on already.
- Those unsual prompts could be very recent event or specialized information it hasn't previously seen. Hence they provide much better responses when they have access to better information.
- This means LLM benefit from a retrieval phase - obtaining specific information - the core idea of RAG.

# How to ensure LLM knows the useful information?
- Key idea is we modify a prompt before sending it to the LLM. In addition to the user's question we can add in information that helps the LLM respond.
- This information needs to be retrieved from somewhere, and the component of RAG system that handles this process is called the **Retriever**. Retriever manages a knowledge base of trusted, relevant, and possibly private information and when RAG receives a prompt, the retriever finds and retrieves the most relevant iformation from the knowledge base to share with the LLM. The model then uses that information when it responds to the prompt.
###### Overall, all we are doing is improving/augmenting the way an LLM generates text.

# Applications of RAG System

- Generating code. While languages have been trained on lots of code, conceivably every public git repo, generating correct code for a specific project requires specialized information, as the LLM needs to know the classes, functions, and definitions in the project as well as the coding style. By retrieving relevant classes, definitions, and files from our repo, an LLM is better able to generate code relevant to the project.
- Customizing chatbots to an individual company. Every company has its own products, policies, and communication guidelines so treating these enterprise documents as a knowledge base allows us to deploy LLM in a variety of useful ways. We could build a customer service chatbot that knows information about the companies products, current inventory, or common troubleshooting steps. We could deploy an internal chatbot that accurately answers questions about company policies or direct you towards useful documentation. Either cases, knowledge base helps ground the LLM response in the company's specific products or policies and minimizes generic or misleading LLM response.
- AI-assisted web search. Historically search engines have worked like a retriever - given a search query, they return relevant websites. Today search engines provide AI summaries of these search results to present the most useful information in skimmable ways. These summaries are basically RAG system whose knowledge base is the entire internet.
- Personalized assistants in text messages, email client, word processor, calender cab biw help send messages, organize schedule, draft documents, etc.

# How LLMS Work

- LLMS are fancy autocompletes as all they do is predict the next word that should appear in a piece of text.
```
What a beautiful day, the sun is ...
```
- If we see this incomplete phrase, we could probably guess what word should complete that sentence, and so could an LLM. Under the hood, LLMs use neural network, an enormous and complex mathematical model of languages and these store information about which words are commonly used with each other, which order they appear, and captures what these words mean in context.
- When an LLM generates a completion, all it's doing is adding new words to the end of the prompt one word at a time. In the example above it would likely add the word **shining** and then add words in the sky one at a time.
- LLMs technically generate tokens, pieces or words. Punctuations could also get their own tokens and most LLMs have a total vocabulary of 10 to more than 100,000 tokens.
- In the above sample, the LLM would process the current state of the completion, generating deep understanding of the relationships between each word and overall meaning. Then it goes through every token in its vocab and uses 10s to 100,000s of them to calculate the probability that it should appear next. Shining would have been the highest probability. The LLM generates a probability distribution across every token then randomly chooses the next token from that probability distribution. In this case for instance, 80 out of 100 times it will choose shining but it is still possible to choose rising or exploding.
- When LLM goes to add another token to the completion, it repeats the entire process.
- An LLM is able to understand the meaning of a prompt and make predictions of words because it has already been trained on large collections of text and the mathematical model that powers an LLM has billions of individual parameters or weights. SO before training, this model would produce gibberish.

# Characteristics of LLMS
- If we asked LLM about our company's private internal data or today's news, the model certainly wasn't trained on that information and in these cases they will provide responses that sound right but aren't actually true. - Although these are called hallucinations, LLMS arent having psychological episode, they are just designed to generate probable text, not truthful text and truth as far as the LLM is concerned is just the sequence of words is probabilistically likely based on its training data.