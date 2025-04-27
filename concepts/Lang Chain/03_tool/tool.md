#  ⚒️ Tools in LangChain
> In LangChain Tools are simple Python **function** with a **schema** that defines function **name**, **description** and **expected args**. Tools can be passed to [chat model](../01_chat_model/chat_model.md) that support [tool calling](./tool_calling.md) allowing the model to request the execution of function with specific output.

## 🔑 Key Concept
* Tools are a way to encapsulate a function and its schema so that it can be passed to a chat model.
* Tools are created using the @tool decorator, supporting the following features:
  1. The chat model automatically infers the tool’s name, description, and expected arguments, while also supporting customization.
  2. Tools can be defined to return artifacts (e.g., images, dataframes, etc.).
  3. Input arguments can be hidden from the schema by using injected tool arguments.

## ♦️ Tool Interface
* The key attribute corresponding to tool's **schema**.
    1. **name**: The name of the Tool
    2. **description**: A Description about of what actually they do.
    3. **args**: Properties that return JSON schema for the tool's args. Optional but required to provide more information or validation.
    4. **return_direct**: Only relevant for agents. if `return_direct` is **True**. it will stop after invoking and return the result directly to the user.

* The key method to execute the function associated to tool
  1. invoke: Invoke the tool with the given args.    
  2. ainvoke: Invokes the tools with given args but **asynchronously**. using [async programming in LangChain](../additionals/async.ipynb)

## Create tools using `@tool` decorator
* The recommended way to create a tool is using [`@tool`](https://python.langchain.com/api_reference/core/tools/langchain_core.tools.convert.tool.html) decorator. The decorator is design to simply the creation and should be used in most cases.

    * [How to create tools](https://python.langchain.com/docs/how_to/custom_tools/)
    > Tool are commonly use in constructing `agents`, you will need to provide list of `tools`.

    * LangChain supports the creation of tools from:
      1. Functions
      2. LangChain Runnables
      3. By sub-class from `BaseTool` -- This is most flexible and customizable method to create tool.
    
    ### 1. Creating tools from Functions
    > This `@tool` is the simples way to define a custom **tool**.The decorator uses the function name as the tool name by default, but this can be overridden by passing a string as the first argument. Additionally, the decorator will use the function's docstring as the tool's description - so a docstring MUST be provided.
    ```python
    from langchain_core.tools import tool

    @tool
    def multiply(a: int, b: int) -> int:
        """Multiply two numbers."""
        return a * b
    
    
    # Let's inspect some of the attributes associated with the tool.
    print(multiply.name)
    print(multiply.description)
    print(multiply.args)
    ```
    * **Note** that `@tool` also supports parsing of`Annotated`, nested schema, and other features.
    ```python
    from langchain_core.tools import tool
    from typing import Annotated, List

    @tool
    def multiply_by_max(
        a:Annotated[int, "Scale factor"]
        b: Annotated[List[int], "list of ints over which take maximum"]
    ) -> int:
    """Multiply a by the max max be""" 
    
    return a * max(b)
    ```