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

    More find from [LangChain API Reference](https://python.langchain.com/api_reference/core/language_models/langchain_core.language_models.chat_models.BaseChatModel.html#)

## 🔠 Input and Output
> Modern LLM's are accessed through chat interface that take [messages](../02_messages/messages.ipynb) as input and return [messages](../02_messages/messages.ipynb) as output. Messages are typically associated with a role (`human`,`system`,`assistant`) and one more content block that contain text or potentially multimodal data (e.g `image`,`video`,`audio`).

> It is most commonly used to provide structured format. that make LLM's to follow this structure that giving the output.

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
> 