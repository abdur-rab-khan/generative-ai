# 💬 Chat Model in LangChain
> Large Language Model (`LLMs`) are advanced machine learning model that are used to perform tasks like **Text Generation**, **Translation**, **Summarization**, **question answering** and more.

> These LLM's are typically work on list of `messages` as a input and produce list of `messages` as output.

- The newest generation chat model also offers some additional capabilities.
    1. **`Tool Calling`**        
        > Modern Chat Model Offer `tool calling` API. The API allow developer to build rich applications that enables LLM's to interact with external Services, API such as Database, Calling Servers to some information. Or We can write custom logic to do something.

    2. **`Structured output`**
        > It is used to say LLM's to give response in this structured format. such as JSON schema that match given schema.

    3. **`Multimodality`**
        > Modern `LLM's` came with `Multimodality`. It is a ability to work with any type of data such as **text**, **image**, **audio** and **video**. Mean that now today LLM's can understand these data.

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

- **More find from** [LangChain API Reference](https://python.langchain.com/api_reference/core/language_models/langchain_core.language_models.chat_models.BaseChatModel.html#)

## 🔠 Input and Output
> Modern LLM's are accessed through chat interface that take [messages](../02_messages/messages.md) as input and return [messages](../02_messages/messages.md) as output.
* Messages are typically associated with a role (`human`,`system`,`assistant`) and one more content block that contain text or potentially multimodal data (e.g `image`,`video`,`audio`).
* It is most commonly used to provide structured format. that make LLM's to follow this structure that giving the output.

* LangChain supports two message formate.
    1. **Lang Chain Message Format**
    2. **OpenAI's Message Format**

| Parameter | Description |
|-----------|-------------|
| `model` | The name or identifier of the specific AI model you want to use (e.g., "gpt-3.5-turbo" or "gpt-4"). |
| `temperature` | Controls the randomness of the model's output. A higher value (e.g., 1.0) makes responses more creative, while a lower value (e.g., 0.0) makes them more deterministic and focused. |
| `timeout` | The maximum time (in seconds) to wait for a response from the model before canceling the request. Ensures the request doesn't hang indefinitely. |
| `max_tokens` | Limits the total number of tokens (words and punctuation) in the response. This controls how long the output can be. |
| `stop` | Specifies stop sequences that indicate when the model should stop generating tokens. For example, you might use specific strings to signal the end of a response. |
| `max_retries` | The maximum number of attempts the system will make to resend a request if it fails due to issues like network timeouts or rate limits. |
| `api_key` | The API key required for authenticating with the model provider. This is usually issued when you sign up for access to the model. |
| `base_url` | The URL of the API endpoint where requests are sent. This is typically provided by the model's provider and is necessary for directing your requests. |
| `rate_limiter` | An optional BaseRateLimiter to space out requests to avoid exceeding rate limits. See rate-limiting below for more details. |

* Chat Model also supports other parameters you can see from there [API Reference](https://python.langchain.com/api_reference/)


## 🔨 Tool Calling
> Chat model can call [tools](../04_tool/tool.ipynb) to perform tasks such as fetching data from database, making API request or can running custom code.

> See the guides of [tool calling](../04_tool/tool_calling.ipynb) for more information.

## 💬 Structured Output
> Chat model can respond structured output in particular format(such as `JSON`, `Custom Schema`) by using [Structured Output](../05_structured_output/structured_output.ipynb).

## 🤹🏻 Multimodality
> Large Language Model (**LLM's**) are not only process `texts`. They can also be used to process other types of data such as **image**, **audio** ,**video**. This is know as [Multimodality](../06_multimodality/multimodality.ipynb).


## 🪟 Context Window
> Context window in term of **Chat Model** is refer to the maximum size of an input that **LLM** can process at a **time**. 
* Modern LLM's came with quite large context size but still **limitation** that must keep in the mind when working with **Chat Model**.
* If the context size exceeds the limit, the model may not be able to process the entire input and cause and error.
* It is very important to manage specially in conversational application, you have to manage how much information the model can **"remember"** throughout a conversation.
* We have to mange the input with the context window to maintain a coherent dialog without exceeding the limit.
* For more details on handling memory in conversation, refer to [memory](../../Lang%20Graph/08_memory/memory.ipynb).

## 🤯 Advanced Topics
### ⌛ Rate-Limiting
> Rate-Limiting is a concept of number of request that can be made at a time period.
* If you hit rate-limit you simple got an error response from the provider, and will need to wait some time before making remove request.

- You have few option to deal with rate limit.
    1. **Try to avoid hitting rate limit by spacing out request**
        - **Chat Models** accept `rate_limiter` parameter that can provided during initializing.
        - The `rate_limiter` parameter is used to control the rate of requests made to the model provider, preventing rate limit errors by ensuring that only a specified number of requests are sent concurrently.
        - Spread out the request to a given model is particularly.
        - See [how to handle rate limits](https://python.langchain.com/docs/how_to/chat_model_rate_limiting/)
    2. **Try to recover from rate limit errors**
        - If we receive a rate limit error, We have to wait a certain amount of time before retrying the request.
        - The amount of time will be increase with each subsequent rate limit error.
        - Chat model have a `max_retries` parameter that can be used to control the number retries
        - See in the [standard parameter](https://python.langchain.com/docs/concepts/chat_models/#standard-parameters)
    3. **Fallback to another chat model**
        - If you hit a rate limit with one chat model, you can switch to another chat model that is not rate-limited.


### 💽 Caching
> Caching is a technique in computer science that is used to store the data in a temporary storage location for faster access.
- Caching a Chat Model response is complex problem and should be approach with caution.
- In Chat Model Caching hit after the first or second iteration in conversation.
- Important Thing is we can't cache the response with exact message. We don't know multiple conversation start with same message.
- So the alternative Approach is to use **semantic caching**, Where we cache the response based on meaning of the message rather than exact message. This could be an approach.
- A **Semantic Caching** introduces a dependency on another model (eg. the semantic caching rely on the [embedding model](https://python.langchain.com/docs/concepts/embedding_models/) to convert text into vector representation) and it's not guaranteed to capture the meaning.
- In some cases Caching chat model response is beneficial. if you have a chat model that is used to answer frequently asked questions, caching responses can help reduce the load on the model provider, costs, and improve response times.
- See [how to cache chat model responses](https://python.langchain.com/docs/how_to/chat_model_caching/)