# Memory in Chat Model

- [Memory in Chat Model](#memory-in-chat-model)
  - [What is Memory?](#what-is-memory)
  - [Type of Memory](#type-of-memory)
    - [Short-term Memory](#short-term-memory)
    - [Long-term Memory](#long-term-memory)

## What is Memory?

- Memory is like a brain of the chat model.
  - It helps them to store, retrieve previous information for better response.
  - Although chat model does not have build-in system to store information.
- As AI Agent, involving complex user interaction equipping with memory.
  - Learn from the feedback.
  - Based on user query they provide adapt the response.

## Type of Memory

- There are two types of memory based on recall.

    1. [Short-term Memory](#short-term-memory)
    2. [Long-term Memory](#long-term-memory)

![types-of-memory](https://langchain-ai.github.io/langgraph/concepts/img/memory/short-vs-long.png)

### Short-term Memory

- **Short-term** or **thread-scoped** memory
  - Can recalled any time within in single conversational thread with a user.
  - It is manages as a agent state (Current state is saved to a database using **CheckPointer**) so the thread can resume any time.
  - Update when --> invoked or step completed
  - State is read at start of each step.

### Long-term Memory

- **Long-term Memory**
  - Shared across any conversational thread.
  - Can be recalled *any time* and in *any thread*.
  - Scoped with any custom namespace not just single thread ID.
