# Vector Store

> Vector Store is a special type of data store, that enable indexing, retrieving information based on vector representations. these vector are called [**embeddings**](../11_embedding/embedding.md/#embedding) which capture sementic meaning of data that has been embedded.

- [Vector Store](#vector-store)
  - [Interface](#interface)
    - [Basic Implementation via `InMemoryVectorStore`](#basic-implementation-via-inmemoryvectorstore)
  - [Integrations](#integrations)
  - [Pinecone](#pinecone)
    - [Credentials](#credentials)
    - [Initialization](#initialization)
    - [Embeddings](#embeddings)
    - [Manage vector store](#manage-vector-store)
      - [Add new items to vector store](#add-new-items-to-vector-store)
      - [Delete items from vector store](#delete-items-from-vector-store)
    - [Query vector store](#query-vector-store)
    - [Query by turning into retriever](#query-by-turning-into-retriever)

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

## [Pinecone](vector_store.ipynb/#pinecone)

- Pinecone is a type of database that helps to store vector data with broader range of  functionality.

### Credentials

- To use **PineCone** vector store you have to first install them **`pip install langchain langchain-pinecone`** and than generate an **"API_KEY"**.

  ```py
  import getpass
  import os
  
  from pinecone import Pinecone
  
  if not os.getenv("PINECONE_API_KEY"):
      os.environ["PINECONE_API_KEY"] = getpass.getpass("Enter your Pinecone API key: ")
  
  pinecone_api_key = os.environ.get("PINECONE_API_KEY")
  
  pc = Pinecone(api_key=pinecone_api_key)
  ```

### Initialization

- Before initialization, let's connect to PineCone **index**. If that named **index** not exist, than will create it.

  ```py
  from pinecone import ServerlessSpec

  index_name = "embeddings-test-index"
  
  if not pc.has_index(index_name):
      pc.create_index(
          name=index_name,
          dimension=1536,
          metric="cosine",
          spec=ServerlessSpec(cloud="aws", region="us-east-1")
      )
  
  index = pc.Index(index_name)
  ```

### Embeddings

- Let's initialize Open AI embedding model and connects with pine cone vector store.

  ```py
  from langchain_openai import OpenAIEmbeddings

  embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
  ```

  ```py
  from langchain_pinecone import PineconeVectorStore

  vector_store = PineconeVectorStore(index=index, embedding=embedding_model)
  ```

### Manage vector store

- After initialization of vector store, let's interact with by adding and deleting different items.

#### Add new items to vector store

- We can add new items to vector store by using **`add_documents`** method.

  ```py
  vector_store.add_documents(documents=documents, ids=uuids)
  ```

#### Delete items from vector store

  ```py
  vector_store.delete(ids=[doc_ids[-1]])
  ```

### Query vector store

- Let's search simple similarity search over vector store.

  ```py
  result = vector_store.similarity_search(
      "LangChain provides abstractions to make working with LLMs easy",
      k=3,  # Number of documents to return, 4 default
      filter={"source": "tweet"},  # Add filtration with the help of metadata
  )
  
  for res in result:
      print(f"--> {res.page_content} [{res.metadata}]")
  ```

- We can also search with score

  ```py
  results = vector_store.similarity_search_with_score(
      "Will it be hot tomorrow?", k=1, filter={"source": "news"}
  )
  for res, score in results:
      print(f"* [SIM={score:3f}] {res.page_content} [{res.metadata}]")
  ```

### Query by turning into retriever

- We can also transform the vector store into a retriever for easier usage in our changes

  ```py
  retriever = vector_store.as_retriever(
      search_type="similarity_score_threshold",
      search_kwargs={"k": 1, "score_threshold": 0.4},
  )
  retriever.invoke("Stealing from the bank is a crime",
                  filter={"source": "news"})
  ```
