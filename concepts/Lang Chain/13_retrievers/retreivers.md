# Retrievers system

> A retrievers system is used to retrieve documents by querying it, we commonly saw in **Vector Database**, **Graph Database** and **Relational Database**. As **AI** going more popular now days, the retrievers system have become more popular (e.g **RAG**), that is used to retrieve relevant document and pass them into **LLM**.

- [Retrievers system](#retrievers-system)
  - [Key Concept](#key-concept)
  - [Interface](#interface)
  - [Common types](#common-types)
    - [Search API's](#search-apis)
    - [Relational or graph database](#relational-or-graph-database)
    - [Lexical search](#lexical-search)
    - [Vector store](#vector-store)
  - [Advanced retrieval patterns](#advanced-retrieval-patterns)
    - [Ensemble](#ensemble)
    - [Source document retention](#source-document-retention)

## Key Concept

- LangChain providers uniform interface for interacting with different type of retrieval system. The LangChain **retrieval** interface is straightforward.

    1. **Input:** A query (string)
    2. **Output:** A list of documents (LangChain [**Document**](https://python.langchain.com/api_reference/core/documents/langchain_core.documents.base.Document.html)).

        ![retrievers-system](https://python.langchain.com/assets/images/retriever_concept-1093f15a8f63ddb90bd23decbd249ea5.png)

## Interface

- The only requirement for retrievers is the ability to accept query and return documents.
- LangChain's retriever class only requires that the **`_get_relevant_documents`** method to be implemented.
  - It takes **`query: str`** as a input and return list of [**Documents**](https://python.langchain.com/api_reference/core/documents/langchain_core.documents.base.Document.html).
  - It use different algorithms under the hood to retrieves the relevant document that matches the query.
- **💀 Note:** It is important to note **LangChain's `retrievers`** is a [**runnable**](../additionals/runnable.md), which allow standard interface which means we have common methods to interact including **`invoke`**.

    ```py
    docs = retriever.invoke(query)
    ```

- Retrievers returns **Document** that have to attribute:
    1. **`page_content`:**
    2. **`metadata`**

## Common types

- There are some common types that are frequently use in **retrievers system**.
  - it is more flexible instead of working with only **vector database**, it also works with **Relational database** where we use **text-to-sql** model that convert simple text query into **sql-query**.

### Search API's

- It's important to note that retrievers don't need to actually ***store*** documents. They serve as a bridge to retrieve the most relevant documents based on a query. **[ the retriever is responsible for querying a backend (like a vector store, database, or external API), not for storing documents. ]**
- We can build retrievers on the top of Common **Search API's** such as **Amazon Kendra** or [**Wikipedia Search**](./retreivers_with_wiki.ipynb).

### Relational or graph database

- Retrievers can also build on the top of **SQL database**. In this cases, [**`query analysis`**]() techniques are used to construct query from natural language (string).
- **Example:** We can build retriever for SQL database using **text-to-SQL** conversion, this allow natural language query (string) to be converted into **SQL QUERY**.

    ```sql
    <!-- Example Query is:- "Show the names of employees who work in the Sales department." -->

    SELECT name
    FROM Employees
    WHERE department = 'Sales';
    ```

  - **Diagram Summary (Logical flow)**

    ```mermaid
    flowchart LR
    A[User Query] --> B[Retriever]
    B --> C[Relevant Schema<br>+ Examples]
    C --> D[Generator]
    D --> E[SQL Output]
    
    B --> F[(Pre-trained Embedding<br>or Index)]
    C --> G[(Template or<br>LLM-based)]

    style F fill:#f24,stroke:#333,stroke-width:1px
    style G fill:#f24,stroke:#333,stroke-width:1px
    ```

- See some retrievers example with [**sql**](./retrievers_with_sql.ipynb).

### [Lexical search](https://python.langchain.com/docs/concepts/retrievers/#lexical-search)

### Vector store

- [**Vector Stores**](../12_vector_store/vector.md) are a popular and efficient way to index and retrieve unstructured data. A vector-store can be used as a retriever by calling the as_retriever() method.

    ```py
    vectorstore = MyVectorStore()
    retriever = vectorstore.as_retriever()
    ```

## Advanced retrieval patterns

### [Ensemble](https://python.langchain.com/docs/how_to/ensemble_retriever/)

- In retrieval system it's possible to combine **multiple retrieval's** using ensemble. the is useful when we are building retrievers that are good at finding different types of relevant documents.
- It is easy to create an ensemble retriever that combines multiple retrievers with linear weighted scores:

    ```py
    # Initialize the ensemble retriever

    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, vector_store_retriever], weights=[0.5, 0.5]
    )
    ```

  - When ensembling, there are some concepts like how do we combine search result from many retrievers?
  - We have the concept of **re-ranking**, which takes the output of multiple retrievers and combines them using a more sophisticated algorithm such as [**Reciprocal Rank Fusion (RRF)**](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf).

### [Source document retention](https://python.langchain.com/docs/concepts/retrievers/#source-document-retention)

- To make easily searchable on any documents, We use some kind of indexing, that is done by **transformation** step (e.g **vector store** often with **text-splitter**).
- Whatever transformation is used, we can easily retain the link between ***transformed document*** and ***original document***, giving the ability to **retrieval** to return **original document.**
  
  ![retriever-system](https://python.langchain.com/assets/images/retriever_full_docs-e6282aafd63f69ab3fcb26b2cfc46b5c.png)

- It is very useful in **AI** application, because ensuring no loss in document context for the model.
- **For Example:** If we use **small chunks** size for indexing the documents in vector store. if we return only the chunks as the retrieval return, It may lost the original document context. to solve this LangChain Provides **two** different retrieval techniques.
  1. [**Multi-Vector Retrieval:**](https://python.langchain.com/docs/how_to/multi_vector/)
      - A Multi-Vector Retrieval is used to
  2. [**ParentDocument Retrieval:**](https://python.langchain.com/docs/how_to/parent_document_retriever/)
      - A ParentDocument Retrieval is used to