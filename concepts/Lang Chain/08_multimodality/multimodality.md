# MultiModality in LangChain

> MultiModality is refers to a ability of model to work with different types of data such as **image**, **video**, **audio**, **text**. It comes in various components.

- **Chat Model**
  - Accept and Generate multimodel input and outputs, handling variety of data such as **text**, **image**, **video**, **audio**.
- **Embedding Model**
  - Embedding Models can represent multimodel content, embedding various form of data such as **text**, **video**, **audio**.
- **Vector Stores**
  - Vector store could search over embeddings that represent multimodel data, enabling to retrieve over different type of information.

- [MultiModality in LangChain](#multimodality-in-langchain)
  - [What kind of multimodality support](#what-kind-of-multimodality-support)

## What kind of multimodality support

### 1. Input

- It is totally depend on model what type of input they support such as **text** (almost all), **image**, **video**, **audio**, **files**

- To pass multimodel input data to a chat model, We have to pass content block that specify the type and corresponding data.

- **Example to pass image**

  ```py
  from langchain_core.messages import HumanMessage

  message = HumanMessage(
      content=[
          {"type": "text", "text": "Describe the weather in this image:"},
          {
              "type": "image",
              "source_type": "url",
              "url": "https://...",
          },
      ],
  )

  response = model.invoke([message])
  ```

- We can pass the image as in data-line

  ```py
  from langchain_core.messages import HumanMessage
  
  message = HumanMessage(
      content=[
          {"type": "text", "text": "Describe the weather in this image:"},
          {
              "type": "image",
              "source_type": "base64",
              "data": "<base64 string>",
              "mime_type": "image/jpeg",
          },
      ],
  )
  response = model.invoke([message])
  ```

- To pass **`PDF`** that are supported by some models such as **Anthropic** than use following configuration.
  - **`source_type`** : **`file`**
  - **`mime_type`** : **`application/pdf`**

- See multimodality from [**here**](https://python.langchain.com/docs/integrations/chat/openai/#multimodal-inputs).

### 2. Output

- Some models are also support multimodality as a output, such as image, audio.
- Here is following example
  - Generating [audio outputs](https://python.langchain.com/docs/integrations/chat/openai/#audio-generation-preview) with OpenAI.
  - Generating [image outputs](https://python.langchain.com/docs/integrations/chat/google_generative_ai/#multimodal-usage) with Google Gemini.
