# 💬 Chat History in LangChain

> Chat History is the conversation but **user**  and **chat model**. It is used to maintain the context and state throughout the conversation. The chat history is sequence of [messages](../02_messages/messages.md/#-messages-in-langchain). each one are associated with a specific [role](../02_messages/messages.md/#role).

## Conversation Pattern

![conversation-pattern](https://python.langchain.com/assets/images/conversation_patterns-0e4c2311b54fae7412f74b1408615432.png)

Most of the conversation starts with [**system message**](../02_messages/messages.md/#1-systemmessage) that contains the context of the conversation. This followed by **`user_message`** containing the user's input, and then an **`assistance message`** containing the response of the model.

The **`assistance`** directly respond to the **`user`** or if configured with tools request that [tool](../03_tool/tool.md/#1-tool) to perform specific tasks.

- A full conversation often involves a combination of two patterns.
    1. The user and **assistance** representing a **back-and-forth-conversation**.
    2. The **assistance** and **tool** message representing an **`"agentic"`** workflows, where the assistant is invoking tools to perform specific tasks.

## Managing the Chat History

> We know that **chat model** have a maximum limit size of input size. it's important to manage the chat history by trimming to avoid the exceeding the [context window](../01_chat_model/chat_model.md/#-context-window).

While processing chat history, it's essential to preserve a correct conversation structure.

- Key guidelines for managing chat history.
    1. The conversation should follow one of these structure.
        - The first message should either a **`system message`** or **`user message`**, followed by **`user message`** than **`assistance message`**.
        - The last message should be either a **`user message`** or **`tool message`** containing the result of the tool call.
    2. When using tool calling, a **`tool`** message should only follow assistance message that request the tool invocation.


- Related Reference
    1. [How to trim a message](./chat_history.ipynb)
    2. [Memory](../../Lang%20Graph/08_memory/memory.md)