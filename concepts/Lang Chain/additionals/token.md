# Tokens

> Modern (**`LLM's`**) are based on transformer architecture that process sequence of units that is knows as tokens. Tokens are the things that models use to break down input and generate outputs.

## What is Tokens

- A **`Token`** is a small piece of text that model uses as its basic units to process, read, generates.
- These **`tokens`** may vary based on model provider defines them, but generally it looks like ⬇️.
  - A whole word (e.g., "apple")
  - A part of a word (e.g., "app")
  - Or other linguistic components such as punctuation or spaces.

- The way models tokenize input is depend upon its **`tokenizer algorithm`**. Which convert user **input** into **token**. Similarly, model's output as a token via stream is decoded into human readable text.

## How Tokens works in language model

- The main reason of using tokens instead of sentences or entire sentences.
  - **Efficiency and Flexibility:** Many words share common prefixes or suffixes. by breaking text into smaller parts, model can handle rare or unknown words better.

### How process works

1. **Input tokenization**

    - When we provide input text ("LangChain is so cool") into the model. the **tokenizer algorithm** breaks text input small pieces.

        ![input-token](https://python.langchain.com/assets/images/tokenization-10f566ab6774724e63dd99646f69655c.png)

2. **Processing**

    - The **`transformer`** architecture behind these model process token sequentially one by one and predict next token (output) by analyzing the relationship between these tokens, capturing context and meaning from the input.

3. **Output generation**

    - The model generate new token one by one and these tokens are than decoded into human readable text.
