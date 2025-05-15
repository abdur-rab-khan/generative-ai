# MultiModality in LangChain

> MultiModality is refers to a ability of model to work with different types of data such as **image**, **video**, **audio**, **text**. It comes in various components.

- **Chat Model**
  - Accept and Generate multimodel input and outputs, handling variety of data such as **text**, **image**, **video**, **audio**.
- **Embedding Model**
  - Embedding Models can represent multimodel content, embedding various form of data such as **text**, **video**, **audio**.
- **Vector Stores**
  - Vector store could search over embeddings that represent multimodel data, enabling to retrieve over different type of information.

- [MultiModality in LangChain](#multimodality-in-langchain)
  - [What kind of multimodality support](#what-kind-of-multimodality-support)

## What kind of multimodality support

### 1. Input

- It is totally depend on model what type of input they support such as **text** (almost all), **image**, **video**, **audio**, **files**

- To pass multimodel input data to a chat model, We have to pass content block that specify the type and corresponding data.

- **Example to pass image**

  ```py
  from lang
  ```

### 2. Output
