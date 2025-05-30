# Embeddings in LangChain

> An Embedding model is very powerful method that enables the conversion of texts---such as **tweets**, **documents** and **books** into numerical representations that machines can understand and compare efficiently. It forms the **cores** of many modern **retrieval systems**. By capturing the **semantic meaning** of text, embeddings allow **search systems** to retrieve relevant content not only through keyword matching but also through a deeper understanding of content and meaning.

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

## Measure similarity

- Embeddings are essentially a set of **coordinates** represented as vectors, often arranged in a matrix. The position of each points in this **coordinates space** reflects the meaning of corresponding text.
- In this **coordinates** space, similar text might to be located close to each other. This proximity allows for intuitive comparison between texts, helping **Language models** to predict answer that are relevant to the input query.
- By converting text into **numerical matrix representations**, We can perform any mathematical operations to quickly measure how two piece of text are---regardless of their original length of structure.
- Some common similarity matrix includes
  1. **Cosine Similarity:**  A metric used to measure how similar two vectors are, based on the angle between them, regardless of their magnitude.
  2. **Euclidean Distance:** Euclidean distance is a measure of the **straight-line** distance between two points in a **multi-dimensional space**
  3. **Dot Product:** An operation in linear algebra that takes two vectors and returns a single scalar value. It reflects how much two vectors point in the same direction
