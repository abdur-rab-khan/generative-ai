# 💬 Messages in LangChain
# Table of Contents

- [💬 Messages in LangChain](#-messages-in-langchain)
- [Table of Contents](#table-of-contents)
  - [What inside the message](#what-inside-the-message)
  - [LangChain Message](#langchain-message)
  - [OpenAI Format](#openai-format)
      - [Output](#output)

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
    *  Depending upon chat model providers. messages can includes other data such as.
        * ID: An optional unique identifier for the message.
        * Name: An optional `name` property which allow to differential between different entities/speakers with the same role.
        * Metadata: Additional information about the message. such as timestamp, token usage etc.
        * Tool Calls: A list tools that request by the modal to call.
    
    ### Conversation Structure
    ```json
    [
        {
            "role":"HumanMessage",
            "content":"How, are you"
        },
        {
            "role":"AIMessage",
            "content":"I'm doing well, how about you?"
        },
        {
            "role":"HumanMessage",
            "content":"Can you tell be a joke."
        },   
        {
            "role":"AIMessage",
            "content":"Sure! Why did the scarecrow win an award? Because he was outstanding in his field!"
        }
    ]
    ```

## LangChain Message
> LangChain provide unified format of message that can be used across any [chat model](../01_chat_model/chat_model.md). allowing users to work with any [chat model](../01_chat_model/chat_model.md) without any worrying.

* There are five types of message:
    1. [**SystemMessage**](#systemmessage)
    2. [**HumanMessage**](#humanmessage)
    3. [**AIMessage**](#aimessage)
    4. [**AIMessageChunk**](#aimessagechunk)
    5. [**ToolMessage**](#toolmessage)

    * **Other important message includes**
        * **RemoveMessage**: Not include any role.This is any abstraction Commonly use in LangGraph to manage the chat history.

    ### 1. SystemMessage
    > A `SystemMessage` is used to supervise the behavior of the chat model by providing additional context, such as instructing the model to adopt a specific tone or characteristics for the conversation (e.g., "The conversation is about cooking").
    
    * Different Chat Provider may support message in a following way.
        1. **Through a `system` message role**
        2. **Through a separated api paramerter**
        3. **No Message support**
       
    ### 2. HumanMessage
    > A `HumanMessage` is corresponds to `user` role. A human message represents input from a user instructing with model.  

    * **Example** 
        ```python
        from langchain_core.messages import HumanMessage
        
        model.invoke([HumanMessage(content="hello, how are you?")])
        ```
    * **Tip**
        * When invoking [chat model](../01_chat_model/chat_model.md) with a string input. LangChain automatically convert it into `HumanMessage`.
    
        #### Multi-model Content
        * Some chat models also accept multi-model data such as **text**,**audio**,**video** or files like **PDFs**.
        
    
    ### 3. AIMessage
    > `AIMessage` is used to represent the response from [chat model](../01_chat_model/chat_model.md) with `assistance` role. which can include `text`, or a request to invoke [`tool`](../04_tool/tool.md). It could also multi-modal type such as (text, video, audio, image).

    * **Example**
        ```python
        from langchain_core.messages import HumanMessage

        ai_message = model.invoke("tell me a joke.")
        ai_message # <--- AIMessage
        ```
    * An `AIMessage` has following attributes. The attributes with are `standardized` are the ones that LangChain attempts to standardized across various [chat model](../01_chat_model/chat_model.md) providers. `raw` fields are specific to the model. 

        | Attribute | Standardized/Raw | Description |
        |-----------|------------------|-------------|
        | `id` | Standardized | An optional unique identifier for the message, ideally provided by the provider/[chat model](../01_chat_model/chat_model.md) that create the message |
        | `content` | Raw | Response from the [chat model](../01_chat_model/chat_model.md) usually a string but can be list of content block |
        | `tool_calls` | Standardized | Tool calls associated with the message. See [`tool_calling`](../04_tool/tool_calling.md) for details |
        | `invalid_tool_calls` | Standardized | Tool calls with errors associated with the massages. See [`tool_calling`](../04_tool/tool_calling.md) for details |
        | `usages_metadata` | Standardized | Usages metadata for a message such as [`token_counts`](../additionals/token.md). See [`Usage Metadata API Reference`](https://python.langchain.com/api_reference/core/messages/langchain_core.messages.ai.UsageMetadata.html). |
        | `response_metadata` | Raw | Response metadata, e.g response headers, logprobs token counts. |

    * A list of A list of dictionaries -- Each dictionary represents a content block and is associated with a type.
        * Used by Anthropic for surfacing agent thought process when doing tool calling.
        * Used by OpenAI for audio outputs. Please see multi-modal content for more information.

    ### 4. AIMessageChunk
    > It is common to stream the response for the [chat model](../01_chat_model/chat_model.md) as they are begin generated, so the user can see the response i real-time instead of waiting for the entire response.

    * It is returned from the `stream`, `astream` and `stream_events` methods of chat models to invoke.
    
    * `AIMessageChunk` structure are same as [`AIMessage`](#3-aimessage). but uses different [`ToolCallChunk`](https://python.langchain.com/api_reference/core/messages/langchain_core.messages.tool.ToolCallChunk.html#langchain_core.messages.tool.ToolCallChunk) to be able to stream tool calling in a standard manner.
    * `AIMessageChunk` also support `+` operator to merge into a single `AIMessage`.

    * **Example**
        ```python      
        from langchain_core.messages import HumanMessage

        ai_message = ""
        for chunk in model.stream([HumanMessage("what is the color of sky")]):
            print(chunk) # Small part of the response 
            ai_message += chunk

        print(ai_message) // Total part of the response
        ``` 
    ### 5. ToolMessage
    > This represent a message with role `tool`. which contains the **results** of [`calling_tool`](../04_tool/tool_calling.md). In additional to `role` and `content`. 
    * This message has:
      1. `tool_call_id`: field that convey the `id` of the call to the tool that was called to produce the result.
      2. `artifact`: field which can be used to pass along arbitrary artifacts of the tool execution which are useful to track but which should not be sent to the model.

    * Please see [**tool_calling**](../04_tool/tool_calling.md) for more information. 

    ### 6. RemoveMessage
    > It is use to manage the [`chat history`](../03_chat_history/chat_history.md) in LangGraph.

    * Please refer following for more information on how to manage `RemoveMessage`:
        1. [Memory concept guide](../../Lang%20Graph/08_memory/memory.md)
        2. [How to delete message](https://langchain-ai.github.io/langgraph/how-tos/memory/delete-messages/) 

## OpenAI Format
> Chat models also accept OpenAI's format as a input to chat models.
```python
chat_model.invoke([
    {
        "role": "user",
        "content": "Hello, how are you?",
    },
    {
        "role": "assistant",
        "content": "I'm doing well, thank you for asking.",
    },
    {
        "role": "user",
        "content": "Can you tell me a joke?",
    }
])
```

#### Output
> The output of the model will be in terms of LangChain messages, so you will need to convert the output to the OpenAI format if you need OpenAI format for the output as well.

* The [`convert_to_openai_messages`](https://python.langchain.com/api_reference/core/messages/langchain_core.messages.utils.convert_to_openai_messages.html) utility function can be used to convert from LangChain messages to OpenAI format.

```python 
from langchain_core.messages import (
    convert_to_openai_messages,
    AIMessage,
    SystemMessage,
    ToolMessage,
)

messages = [
    SystemMessage([{"type": "text", "text": "foo"}]),
    {"role": "user", "content": [{"type": "text", "text": "whats in this"}, {"type": "image_url", "image_url": {"url": "data:image/png;base64,'/9j/4AAQSk'"}}]},
    AIMessage("", tool_calls=[{"name": "analyze", "args": {"baz": "buz"}, "id": "1", "type": "tool_call"}]),
    ToolMessage("foobar", tool_call_id="1", name="bar"),
    {"role": "assistant", "content": "thats nice"},
]
oai_messages = convert_to_openai_messages(messages)

# -> [
#   {'role': 'system', 'content': 'foo'},
#   {'role': 'user', 'content': [{'type': 'text', 'text': 'whats in this'}, {'type': 'image_url', 'image_url': {'url': "data:image/png;base64,'/9j/4AAQSk'"}}]},
#   {'role': 'assistant', 'tool_calls': [{'type': 'function', 'id': '1','function': {'name': 'analyze', 'arguments': '{"baz": "buz"}'}}], 'content': ''},
#   {'role': 'tool', 'name': 'bar', 'content': 'foobar'},
#   {'role': 'assistant', 'content': 'thats nice'}
# ]
```