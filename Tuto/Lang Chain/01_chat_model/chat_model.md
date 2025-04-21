# 💬 Chat Model in LangChain
> Large Language Model (`LLMs`) are advanced machine learning model that are used to perform tasks like **Text Generation**, **Translation**, **Summarization**, **question answering** and more.

> These LLM's are typically work on list of `messages` as a input and produce list of `messages` as output.

- The newest generation chat model also offers some additional capabilities.
    1. **`Tool Calling`**        
        > Modern Chat Model Offer `tool calling` API. The API allow developer to build rich applications that enables LLM's to interact with external Services, API such as Database, Calling Servers to some information.

    2. **`Structured output`**
        > It is used to say LLM's to give response in this structured format. such as JSON schema that match given schema.

    3. **`Multimodality`**
        > It is a ability to work with any type of data such as **text**, **image**, **audio** and **video**.

## ⭐ Key Methods
- The key method of chat model are:
    1. **`invoke`**

        > It is primary method to interact with chat model, it is starting point. It take list of `messages` as input and respond list of `messages` as output.
    2. **`stream`**

        > A stream method is used to steam that output from the chat model, chuck by chunk.
    3. **`batch`**

        > A method that is used to run multiple requests to a chat model simultaneously to get responses together for more efficient processing.
    4. **`bind_tools`**
        
        > A method that allows us to bind tools to the chat model. This gives context (about the tools) to the model which helps it during execution.

    5. **`with_structured_output`**

        > A wrapper around the `invoke` method for models that natively support `structured output`.

    More find from [](https://python.langchain.com/api_reference/core/language_models/langchain_core.language_models.chat_models.BaseChatModel.html#)