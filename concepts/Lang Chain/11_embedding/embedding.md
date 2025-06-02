# Embeddings in LangChain

> An Embedding model is very powerful method that enables the conversion of texts---such as **tweets**, **documents** and **books** into numerical representations that machines can understand and compare efficiently. It forms the **cores** of many modern **retrieval systems**. By capturing the **semantic meaning** of text, embeddings allow **search systems** to retrieve relevant content not only through keyword matching but also through a deeper understanding of content and meaning.

- [Embeddings in LangChain](#embeddings-in-langchain)
  - [Key concepts](#key-concepts)
  - [Embedding](#embedding)
    - [Interface](#interface)
    - [Measure similarity](#measure-similarity)
  - [Embedding Model](#embedding-model)
  - [Text Embedding Model](#text-embedding-model)
  - [Caching](#caching)

## Key concepts

![embedding-in-lang-chain](https://python.langchain.com/assets/images/embeddings_concept-975a9aaba52de05b457a1aeff9a7393a.png)

---

1. **Embed text as a vector:** Embedding model transform text into a numerical vector representation.
2. **Measure similarity:** Embedding vectors can be compared using simple **mathematical operations.**

## Embedding

### Interface

- LangChain provides common interface for working with them, providing standard methods for common operators. These common interface simplifies interaction with various embedding providers through two main methods.

1. **`embed_documents`:** It converts list of texts into vector representation.

    ```py
    from langchain_openai import OpenAIEmbeddings
    
    # Practical example to embed list of string.
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
    embedding = embedding_model.embed_documents(
        [
            "Hi there!",
            "Oh, hello!",
            "What's your name?",
            "My friends call me World",
            "Hello World!"
        ]
    )
    
    len(embedding), len(embedding[0])
    ```

2. **`embed_query`:** It converts single texts (query) into vector representation.

    ```py
    query_embedding = embeddings_model.embed_query("What is the meaning of life?")
    doc_embedding = embeddings_model.embed_documents([
        "What is the meaning of life?"
    ])

    print(len(query_embedding)) # 1536
    print(len(doc_embedding[0])) # 1536
    ```

- LangChain provides many embedding models you can find them from [**here**](https://python.langchain.com/docs/integrations/text_embedding/).

### Measure similarity

- Embeddings are essentially a set of **coordinates** represented as vectors, often arranged in a matrix. The position of each points in this **coordinates space** reflects the meaning of corresponding text.
- In this **coordinates** space, similar text might to be located close to each other. This proximity allows for intuitive comparison between texts, helping **Language models** to predict answer that are relevant to the input query.
- By converting text into **numerical matrix representations**, We can perform any mathematical operations to quickly measure how two piece of text are---regardless of their original length of structure.
- Some common similarity matrix includes
  1. **Cosine Similarity:**  A metric used to measure how similar two vectors are, based on the angle between them, regardless of their magnitude.
  2. **Euclidean Distance:** Euclidean distance is a measure of the **straight-line** distance between two points in a **multi-dimensional space**
  3. **Dot Product:** An operation in linear algebra that takes two vectors and returns a single scalar value. It reflects how much two vectors point in the same direction.

## [Embedding Model](./embedding.ipynb/#embedding-model)

> Embedding model are responsible to create vector representation of a piece of text, [See](https://python.langchain.com/docs/integrations/text_embedding/#all-embedding-models)

## [Text Embedding Model](./embedding.ipynb/#text-embedding-models)

- Embedding create a **vector** representation of a piece of text, It plays very important role in terms of searching over vector such as **semantic search** where we look for a piece of text that are most similar in the vector store.
- The base **`Embedding`** class provides two method.
    1. **`.embed_query`:** It takes list of **`text`** as an input, return list of **`floats`**.
    2. **`.embed_documents`:** It takes single text as an input, return list of lists of **`floats`**.

## [Caching](./embedding.ipynb/#caching)

- Caching in embedding can be stored or temporarily cached to avoid need of re-computation.
- It can done using **`CacheBackedEmbeddings`**, The cache embedder is wrapper around an embedder that cache embedding in a key-value store.
- The text is hashed and the hash is used as the key in the cache.

The main supported way to initialize a CacheBackedEmbeddings is from_bytes_store. It takes the following parameters:

- **`underlying_embedder:`** The embedder to use for embedding.
- **`document_embedding_cache`:** Any ByteStore for caching document embeddings.
- **`batch_size`**: (optional, defaults to None) The number of documents to embed between store updates.
- **`namespace`:** (optional, defaults to "") The namespace to use for document cache. This namespace is used to avoid collisions with other caches. For example, set it to the name of the embedding model used.
- **`query_embedding_cache`:** (optional, defaults to None or not caching) A ByteStore for caching query embeddings, or True to use the same store as document_embedding_cache.

- **💀 Note**:
  - Be sure to set the **`namespace`** parameter to avoid collisions of the same text embedded using different embeddings models.
  - **`CacheBackedEmbeddings`** does not cache query embeddings by default. To enable query caching, one needs to specify a **`query_embedding_cache`**.
