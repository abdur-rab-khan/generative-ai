# 💬 Messages in LangChain
> Messages in LangChain is the core component that represent the input and output of a [chat model](../01_chat_model/chat_model.md). as well as it is also used to give the context or meta data about the conversation.

* So usually messages are come with role (`system`,`human`,`assistance`) and content (`text`, `multimodal data`) with additional meta data that varies on the chat model.
* LangChain message are build like that, that can be used across any chat model. Allowing users to work with different chat model without worrying.

## What inside the message
* So message have following information
    1. [role](#🎭-role): The role of the message (e.g `human`,`system`)
    2. [content](#🧾-content): The piece of information(eg `text`, `multimodal data`)
    3. [Additional metadata](#additional-metadata): metadata:id, token usage and other model-specific data.

### 🎭 Role
> Role is used to distinguish between different type of messages in a conversation and help chat model to response according to them.

| Role | Description |
|------|-------------|
| `system` | Used to tell chat model how to behave and make response according to system message. Not supported by all chat model providers. |
| `user` | It is nothing but user input. usually in the form of text. |
| `assistant` | It represent the response from chat model. we can include text or request to invoke tools |
| `tool` | A message used to pass the results of a tool invocation back to the model after external data or processing has been retrieved. User with chat models that support [tool calling](../04_tool/tool_calling.md) |

### 🧾 Content
> The content of a message can be text, list of dictionaries representing multimodal data. The exact format can be vary between different chat model providers. Currently only some models are support multimodal data.

* For more information see:
    * [SystemMessage]()
    * [HumanMessage]()
    * [AIMessage]()
    * [Multimodality]()
    
    ### Other Message Data
    * Depending upon chat model providers. messages can includes other data such as.
      * ID: An optional unique identifier for the message.
      * Name: An optional `name` property which allow to differential between different entities/speakers with the same role.
      * Metadata: Additional information about the message. such as timestamp, token usage etc.
      * Tool Calls: A list tools that request by the modal to call.

###  Additional metadata 