
# Tool calling in LangChain

> Many AI Applications interact with humans directly. It is must for model to response in a natural language that human can understand. But what about cases where we want a model to also directly interact with ***system***, such as **Databases**, or an **API**. To interact with these systems we have to use ***API's*** with required payload **structure**. For this kind of mechanism we use [tool calling](https://platform.openai.com/docs/guides/function-calling/example-use-cases?api-mode=responses).

- [Tool calling in LangChain](#tool-calling-in-langchain)
  - [Key concepts](#key-concepts)
    - [Tool binding](#tool-binding)
    - [Tool calling](#tool-calling)
    - [Tool Execution](#tool-execution)
  - [Best practices](#best-practices)

![Tool calling](https://python.langchain.com/assets/images/tool_calling_concept-552a73031228ff9144c7d59f26dedbbf.png)

- Model can directly give the response to the user.
- Model can also call tool that call the systems, such as ***Database*** with required payload.

## Key concepts

![tool-calling-workflow](https://python.langchain.com/assets/images/tool_calling_components-bef9d2bcb9d3706c2fe58b57bf8ccb60.png)

- **Tool Calling Workflow**

    1. [Tool Creation](./tool.md)
        - Creating a tool using `@tool` decorator, It is a simple function that run custom code to get the result based on payload from the system.  
    2. [Tool binding](#tool-binding)
        - The tools needs to connect to the model that support `tool calling`, This gives model awareness of the tool and the associated input schema required by the model.
    3. Tool calling
        - The model decides to call the tool its response follow to the tool's input schema.
    4. Tool Execution
        - Finally, Tool can be executed using the arguments provided by the model.

### Tool binding

> The important thing in LangChain provides standardize interface for connecting tools with model. The `model.bind_tools(list_tools)` method are used to specify the model of available tools.

- **Example**

    ```python
    from langchain_core.tools import tool

    @tool
    def multiply(a: int, b: int):
        """Multiply two numbers"""

        return a * b

    model_with_tools = model.bind_tools(multiply)

    model_with_tools.invoke("what is 2 multiply by 2.")
    ```

  - `bind_tools(list_tools)` list of tools or single tool are a arguments.

### Tool calling

> A key principle of tools calling is model decides when to use a tool based on input's relevance. the model doesn't need to call tool always. For example unrelated input, the model would not call tools.

![tool-calling](https://python.langchain.com/assets/images/tool_call_example-2348b869f9a5d0d2a45dfbe614c177a4.png)

- **Examples**

  ```python
  result = model_with_tools("hello world")
  ```
  
  - The result would be an [`AIMessage`](../02_messages/messages.md/#3-aimessage)  containing the response in natural language (e.g "Hello"). if we pass an input *relevant* to the model. the model should choose which tool have to call it.

    ```python
    result = model_with_tools("what is 2 multiply by 5.")
    ```

  - Here also message will be an [`AIMessage`](../02_messages/messages.md/#3-aimessage) But, if tool is called, result will have a `tool_attribute`. The attributes includes everything needed to execute the tool. including `tool name`, `tool arguments`.

    ```shell
    result.tool_calls
    {'name': 'multiply', 'args': {'a': 2, 'b': 3}, 'id': 'xxx', 'type': 'tool_call'}
    ```

### Tool Execution

> Tools are implement on the runnable interface, which means that they can be invoked e.g `tool.invoke(args)`, `tool.ainvoke(args)` (for asynchronous).

## Best practices

- When designing a tool used by the model, keep the following in mind:
  
  1. Tools are should be well named, correctly-documented and properly type-hinted are make easier for the model.
  2. Design simple and narrowly scoped (very specific task), as they are easier for the model to use.
  3. Use chat models that support [tool calling](./tool_calling.md)
