# Structured Output

> We know that, Chat Model always respond in a **natural languages**. However, there are some scenarios where we need to respond in a structured way. For Example, we might want to store response data into the **database**  and ensure that the output conforms the database schema. So in this situation **Structured Output** came into the picture.

![structured-output](https://python.langchain.com/assets/images/structured_output-2c42953cee807dedd6e96f3e1db17f69.png)

- [Structured Output](#structured-output)
  - [Key concepts](#key-concepts)
    - [Recommended usage](#recommended-usage)
    - [Schema Definition](#schema-definition)
    - [Returning Structured output](#returning-structured-output)
      - [1. Using tool calling](#1-using-tool-calling)
      - [2. JSON model](#2-json-model)
      - [3. Structured output method](#3-structured-output-method)

## Key concepts

### Recommended usage

> This pseudocode illustration the recommended workflow when using structured output.  LangChain provides a method, [**`with_structured_output()`**](./structured_output.ipynb), that automates the process of binding the schema to the model and parsing the output. This helper function is available for all model providers that support structured output.

```py
#Define Schema

schema = {"foo": "bar"}

# Bind Schema to model
model_with_structured_output = model.with_structured_output(schema)

# Invoke the model to produce structured output that matches the schema
structured_output = model_with_structure.invoke(user_input)
```

### Schema Definition

> The output schema is represent as a schema, which can be defined in several ways.

- The output structure of model response needs to represent in some way.
- While types of objects you can use depend on the model you're working with, there are some common types of object that are typically allowed.
- The simplest and most common format for structured output is a **JSON** like structured, which in python is represent as **dict** or **list**.
- **JSON** object are often used directly when the tool require raw, flexible and minimal overhead.

```py
{
  "answer": "the answer to the user's question",
  "followup_question": "A followup question the user could ask"
}
```

- We can also use **Pydantic** to define the structured output.
- Using **Pydantic**, Pydantic is particularly useful for defining structured output schemas because it offers type hints and validation

```py
from pydantic import BaseModel, Field

class ResponseFormatter(BaseModel):
    answer:str =  Field(description = "the answer to the user's question")
    followup_question = Field(description = "A followup question the user could ask")
```

### Returning Structured output

> The model is given this schema, and instructed to return output in that format.

- We need a way to instruct model to use that structured output schema.
  - While one approach is to include this schema in the prompt and *ask nicely* for the model to use it.
  - Several but several more powerful methods are there that utilizes navtive features in the model provider's API are available.

#### 1. Using tool calling

> The central concept is straightforward: ***simply bind the schema to a model as a tool!***, Here is the example using **`ResponseFormatter`** schema defined above.

- We know that many model's supports tool calling, In short tool calling involves binding tool to a model and when appropriate, the model can decided to call this tool and ensure the response conforms to the tool's schema.

- **Example**

    ```py
    from langchain_openai import ChatOpenAI

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # Bind ResponseFormatter schema as tool to the model
    model_with_tools = model.bind_tools([ResponseFormatter])
    
    ai_message = model_with_tools.invoke("what is the powerhouse of cell")

    ai_message.tool_calls[0]["args"]

    # Parse the dictionary into a pydantic object
    pydantic_object = ResponseFormatter.model_validate(
        ai_message.tool_calls[0]["args"])
    
    print(pydantic_object)
    ```

  - **Output**

    ```shell
    answer="The powerhouse of the cell is the mitochondrion. Mitochondria are organelles that generate most of the cell's supply of adenosine triphosphate (ATP), which is used as a source of chemical energy. They are also involved in other important processes such as the regulation of the cell cycle and cell growth." followup_questions='What are the functions of mitochondria?'
    ```

#### 2. JSON model

> Any model support a feature call **`json mode`**. The support defining schema as a input and enforces the model to produce a conforming JSON output. You can see on the table which model support [here](https://python.langchain.com/docs/integrations/chat/).

- **Example**

    ```py
    from langchain_openai import ChatOpenAI

    model = ChatOpenAI(
        model="gpt-4o-mini").with_structured_output(method="json_mode")
    
    ai_msg = model.invoke(
        "Return a JSON object with key 'random_ints' and a value of 10 random ints in [0-99]")
    
    ai_msg
    ```

  - **Output**

    ```shell
    {'random_ints': [34, 72, 18, 56, 89, 7, 43, 21, 66, 5]}
    ```

#### 3. Structured output method

- There are some challenges in the above method when producing structured output.
    1. When using tool calling, tool call arguments need to be parsed from dictionary back to the original schema.
    2. In addition, the method needs to instruct to *always* use when we want to enforce structured  output.
    3. When JSON mode is used, the output needs to be parsed into a JSON object.

- With these challenges in mind, LangChain provides a helper function (with_structured_output()) to streamline the process. Here we pass schema as input which specifies the names, types, and description of the desire output attributes.

    ![structured-output](https://python.langchain.com/assets/images/with_structured_output-4fd0fdc94f644554d52c6a8dee96ea21.png)

- **Example**

    ```py
    from langchain_openai import ChatOpenAI

    model_with_structure = ChatOpenAI(
        model="gpt-4o-mini").with_structured_output(ResponseFormatter)
    
    # Invoke the model
    structured_output = model_with_structure.invoke(
        "What is the powerhouse of the cell?")
    
    # Get back the pydantic object
    structured_output
    ```

  - **Output**

    ```shell
    ResponseFormatter(answer="The powerhouse of the cell is the mitochondrion (plural: mitochondria). Mitochondria are organelles that generate most of the cell's supply of adenosine triphosphate (ATP), used as a source of chemical energy. They are often referred to as the powerhouse because they play a crucial role in energy production through the process of cellular respiration.", followup_questions='What other functions do mitochondria have in the cell?')
    ```

- For better understanding see [here](../apps/joke_generator/joke_generator.ipynb)