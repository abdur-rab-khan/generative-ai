# Text splitters in LangChain

> **Text splitters** is a functionality that breaks down whole sentences into to smaller tokens (chunks). e.g ("LangChain is cool") **Text splitters** breaks like that ["Lang", "Chain", "is", "cool"].

- By **splitting** large document into small chunk without losing the context and meaning.
- There are several techniques to split documents each with its own **advantages**.
- Text splitters split documents into smaller chunks for use in downstream applications.

    ![text-splitters](https://python.langchain.com/assets/images/text_splitters-7961ccc13e05e2fd7f7f58048e082f47.png)

- [Text splitters in LangChain](#text-splitters-in-langchain)
  - [Why split documents](#why-split-documents)
  - [Approaches](#approaches)
    - [1. Length Based](#1-length-based)
      - [1. Token-Based](#1-token-based)
      - [2. Character-Based](#2-character-based)
    - [2. Text-structure Based](#2-text-structure-based)
    - [3.  Document-structure Based](#3--document-structure-based)
    - [4. Semantic meaning Based](#4-semantic-meaning-based)

## Why split documents

- Suppose we have large document.
    1. **Handling none-uniform document lengths:** So in the large documents we many large number of texts. By splitting ensures consistent processing across all documents.
    2. **Context Window:** Many Embedding Models and language model can have large context window but they have limitation. By splitting we can process large document otherwise exceeds the limits.
    3. **Time and Model:** Passing large document directly into the model can raise **time and money**.
    4. **Improve representation quality:** For longer documents, the quality of embeddings may degrade as they try to capture more information. Splitting can lead to more focus and accurate representation.
    5. **Enhancing retrieval precision:** In information retrieval system, splitting text can improve the search result, allowing more precise matching of queries.
    6. **Optimizing computational resources**: Working with smaller chunks of text can be more memory-efficient and allow for better parallelization of processing tasks.

## Approaches

- **💀 Note:** When you count tokens in your text you should use same to tokenizer as used in the language model.

### 1. Length Based

- The most easy way to split document is based on their length. This is simple and most effective approach the ensures that the length does not exceed a specifies size.
- Key benefits are
  - Straightforward implementation
  - Consistent chuck size
  - Easily adaptable with different models

- There are two main types of length-based splitting.
  - **Token-Based:** It is useful when working with language model.
  - **Character-Based** It can be more consistent across different text.

#### 1. Token-Based

- The conversion is based upon number of tokens instead of characters, the is most preferred in **RAG**, **QA**, **chat** application.
- **Example**
  - Character Split (**`chunk_size=10`**)

    ```py
    "The quick "
    "brown fox "
    "jumps over"
    " the lazy "
    "dog."
    ```

  - Token Split (**`chunk_size=10`** using `tiktoken`)

    ```py
    ["The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog", "."]
    → 1 chunk (10 tokens)
    ```

- **Based on token using `tiktoken`**

  ```py
  from langchain.text_splitter import TokenTextSplitter
  
  # Define the token splitter
  token_splitter = TokenTextSplitter.from_tiktoken_encoder(
      encoding_name="cl100k_base",
      chunk_size=1000,
      chunk_overlap=400
  )
  
  token_chunks = token_splitter.split_text(docs)
  
  print(f"Token-based: {len(token_chunks)} chunks")
  print(token_chunks[0])
  ```

  - In **`.from_tiktoken_encorder()`**
    - It takes **`encoding_name`** eg **"`cl100k_base`"** or **`model_name`** eg **"`gpt-4`"**
  - **`chunk_size`** define the size of token.
  - **`chunk_overlap`** defines the how many characters or tokens from the end of one chunk repeat at beginning of the next chunk.
  
#### 2. Character-Based

- The **split** is based on give character sequence by default it is **`"\n\n"`**. Chunk length is measured by number of the characters.

  ```py
  from langchain.text_splitter import CharacterTextSplitter
  
  print("Total length of the docs is:- ", len(docs))
  # Define the character splitter
  char_splitter = CharacterTextSplitter(
      separator="\n",
      chunk_size=1000,      # each chunk has 1000 characters
      chunk_overlap=200,     # each chunk overlaps 100 characters with the previous
      length_function=len,
      is_separator_regex=False
  )
  
  char_chunks = char_splitter.split_text(docs)
  print(f"Len chunks: {len(char_chunks)}")
  print(f"Char chunk: {char_chunks[0]}")
  ```

- It you want to add metadata associated with each chunk use **`.create_documents`**

  ```py
  doc_chunk = char_splitter.create_documents(
    [char_chunks[0]], metadatas=[metadatas[0]])

  print(doc_chunk)
  ```

### 2. Text-structure Based

- Text is naturally organized into hierarchal unit such as **sentences**, **paragraphs**, **word**. We can leverage this structure in splitting strategy, creating split that maintain natural language flow. We can use **`RecursiveCharacterTextSplitter`** to implement this concept.

  - The default strategy is:
    - Paragraphs (**`\n\n`**)
    - Sentences (**`\n`**)
    - Words (**`" "`**)

  - It provide flexibility when token size is exceed there limit.
    - Try to preserve into **paragraphs** (if exceeded).
    - Try to preserve into **Sentence** (if exceeded).
    - Try to preserve into **Words**

### 3.  Document-structure Based

### 4. Semantic meaning Based
