# Prompt Template

> Prompt Template help to translate user input and parameters into instructions for a language model. The can be used to guide a model's response, helping it understand the context and generate relevant output.

- [Prompt Template](#prompt-template)
  - [String PromptTemplates](#string-prompttemplates)
  - [ChatPromptTemplates](#chatprompttemplates)
  - [MessagesPlaceHolder](#messagesplaceholder)

## String PromptTemplates

> These prompt templates are used to format a single string, and generally are used for simpler inputs.

- **Example**

    ```py
    from langchain_core.prompts import PromptTemplate
    
    prompt_template = PromptTemplate.from_template("Tell me a joke about {topic}")
    
    prompt_template.invoke({"topic": "cats"})
    ```

## ChatPromptTemplates

> These templates are used to format list of messages. These "templates" consists of a list of templates themselves.

- **Example**

    ```py
    from langchain_core.prompts import ChatPromptTemplate
    
    prompt_template = ChatPromptTemplate([
        ("system", "You are a helpful assistant"),
        ("user", "Tell me a joke about {topic}")
    ])
    
    prompt_template.invoke({"topic": "cats"})
    ```

  - There are two messages in the above example, The first is [`SystemMessage`](../02_messages/messages.md/#1-systemmessage) that has no variable to format. The second message is a [`HumanMessage`](../02_messages/messages.md/#2-humanmessage), and will be formatted by `topic` variable.

## MessagesPlaceHolder

> As we see above prompt templates are responsible to add list of messages in a particular place. Same as `MessagePlaceHolder` is used to add list of messages that we would slot into a particular spot.

- **Example**

    ```py
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.messages import HumanMessage
    
    prompt_template = ChatPromptTemplate([
        ("system", "You are a helpful assistant"),
        MessagesPlaceholder("msgs")
    ])
    
    prompt_template.invoke({"msgs": [HumanMessage(content="hi!")]})
    ```

  - This will produce two messages, first one is `SystemMessage`, and the second one is `HumanMessage`. In total we have two messages.

  - There is alternative approach without using `MessagePlaceHolder`.

    ```py
    prompt_template = ChatPromptTemplate([
        ("system", "You are a helpful assistant"),
        ("placeholder", "{msgs}") # <-- This is the changed part
    ])
    ```
