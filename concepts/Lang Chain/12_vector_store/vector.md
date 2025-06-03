# Vector Store

> Vector Store is a special type of data store, that enable indexing, retrieving information based on vector representations. these vector are called [**embeddings**](../11_embedding/embedding.md/#embedding) which capture sementic meaning of data that has been embedded.

- [Vector Store](#vector-store)
  - [Interface](#interface)
    - [Basic Implementation via `InMemoryVectorStore`](#basic-implementation-via-inmemoryvectorstore)
  - [Integrations](#integrations)
    - [Pinecone](#pinecone)

![vector-store](https://python.langchain.com/assets/images/vectorstores-2540b4bc355b966c99b0f02cfdddb273.png)

## Interface

- LangChain provides a standard interface for working with Vector Store. Allowing us to switch between different vector store.

The interface consist of basic methods for **Creating**, **Deleting**, **Searching** for documents in the vector store.

- The key method are:
  1. **`add_documents:`** Add a list of texts in the vector store.
  2. **`delete:`** Delete the list documents from the vector store.
  3. **`similarity_search:`** Search for similar documents.

### [Basic Implementation via `InMemoryVectorStore`](./vector_store.ipynb/#basic-implementation-via-inmemoryvectorstore)

- Most of the vector store in LangChain accept embedding model as an argument during initialization.

  - Initializing with an embedding model.

    ```py
    from langchain_openai import OpenAIEmbeddings
    from langchain_core.vectorstores import InMemoryVectorStore
    
    # Initializing with an embedded model
    vector_store = InMemoryVectorStore(
        OpenAIEmbeddings(model="text-embedding-3-small"))
    ```

- [Add Documents](./vector_store.ipynb/#add-documents)
- [Delete Documents](./vector_store.ipynb/#delete)
- [Search Documents](./vector_store.ipynb/#search)

## Integrations

- LangChain provides large number of **vector stores** integration, that is used stores embedded data and perform similarity search.

### Pinecone
