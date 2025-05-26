# Text splitters in LangChain

> **Text splitters** is a functionality that breaks down whole sentences into to smaller tokens (chunks). e.g ("LangChain is cool") **Text splitters** breaks like that ["Lang", "Chain", "is", "cool"].

- By **splitting** large document into small chunk without losing the context and meaning.
- There are several techniques to split documents each with its own **advantages**.
- Text splitters split documents into smaller chunks for use in downstream applications.

    ![text-splitters](https://python.langchain.com/assets/images/text_splitters-7961ccc13e05e2fd7f7f58048e082f47.png)

- [Text splitters in LangChain](#text-splitters-in-langchain)
  - [Why split documents](#why-split-documents)

## Why split documents

- Suppose we have large document.
    1. **Handling none-uniform document lengths:** So in the large documents we many large number of texts. By splitting ensures consistent processing across all documents. 
    2. **Context Window:** Many Embedding Models and language model can have large context window but they have limitation. By splitting we can process large document otherwise exceeds the limits.
    3. **Time and Model:** Passing large document directly into the model can raise **time and money**.
    4. **Improve representation quality:** For longer documents, the quality of embeddings may degrade as they try to capture more information. Splitting can lead to more focus and accurate representation.
    5. **Enhancing retrieval precision:** In information retrieval system, splitting text can improve the search result, allowing more precise matching of queries.
    6. **Optimizing computational resources**: Working with smaller chunks of text can be more memory-efficient and allow for better parallelization of processing tasks.

## Approaches

