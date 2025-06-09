# Retrieval

> We know about [**retrievals**](./retreivers.md) in depth, it is a system that identifying the relevant document from large dataset (**databases**). it commonly used with various data format.

- [Retrieval](#retrieval)
  - [Overview](#overview)
  - [Key Concepts](#key-concepts)
  - [Query analysis](#query-analysis)

## Overview

- There are two common data format that **retrievals** system accommodate.
  - **Un-Structured:** is often store in a **vector** databases or **lexical** search index.
  - **Structured data:** is typically store in **relational** or **vector** database.

- As today, there are multiple types of data format. Modern **AI** increasing aim to make all types of data accessible through natural language interface.
- It try to process **natural language query** into formats compatible with underlying search index or database.

## Key Concepts

![retrieval-system](https://python.langchain.com/assets/images/retrieval_concept-2bcff1b2518f194b34eaf472ac748ffa.png)

1. **Query analysis:** A process where model construct or transform **natural language query** into search query for optimize **retrieval.**
2. **Information retrieval:** Search query are used to fetch information from **different retrieval system**.

## Query analysis

