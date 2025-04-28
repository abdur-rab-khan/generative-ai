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
      2. LangChain [Runnables](../additionals/runnable.md)
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
    * **Note** that `@tool` also supports parsing of [`Annotated`](../additionals/annotated.ipynb), nested schema, and other features.
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
    * Also we can **customize** **tool name** and JSON args by passing them into the tool decorator

      ```python
      from pydantic import BaseModel, Field
      
      
      class CalculatorInput(BaseModel):
          a: int = Field(description="first number")
          b: int = Field(description="second number")
      
      
      @tool("multiplication-tool", args_schema=CalculatorInput, return_direct=True)
      def multiply(a: int, b: int) -> int:
          """Multiply two numbers."""
          return a * b
      
      
      # Let's inspect some of the attributes associated with the tool.
      print(multiply.name)
      print(multiply.description)
      print(multiply.args)
      print(multiply.return_direct)
      ```

  * **Docstring parsing**
    > `@tool` can optionally parse [Google Style docstring](https://google.github.io/styleguide/pyguide.html#383-functions-and-methods) and associated docstring like(such as args description).
    ```python 
    @tool(parse_docstring=True)
    def foo(bar: str, baz: int) -> str:
        """The foo.
    
        Args:
            bar: The bar.
            baz: The baz.
        """
        return bar
    
    
    print(foo.args_schema.model_json_schema())
    ```
    * Output
    ```json
    {
      'description': 'The foo.',
      'properties': {'bar': {'description': 'The bar.',
        'title': 'Bar',
        'type': 'string'},
        'baz': {'description': 'The baz.', 'title': 'Baz', 'type': 'integer'}},
      'required': ['bar', 'baz'],
      'title': 'fooSchema',
      'type': 'object'
    }
    ```
    *  StructuredTool
    > `StructuredTool.from_function` class method provide bit more configurability than `@tool` decorator with any complex code.
    ```python
    from langchain_core.tools import StructuredTool

    def multiply(a: int, b: int) -> int:
      """Multiply two numbers"""
      return a * b

    async def amultiply(a: int, b: int) -> int:
      """Multiply two numbers"""
      return a * b


    calculate = StructuredTool.from_function(func=multiply, coroutine=amultiply)

    print(calculate.invoke(5,5))
    print(await calculate.ainvoke(5,5))
    ```
    * [**API Reference**](https://python.langchain.com/api_reference/core/tools/langchain_core.tools.structured.StructuredTool.html)

    * To configure it:
      ```python
      from pydantic import BaseModel, Field
      from langchain_core.tools import StructuredTool
  
      class CalculateInput(BaseModel):
          a: int = Field(description="first number")
          b: int = Field(description="second number")
      
      
      def multiply(a: int, b: int) -> int:
          """Multiply two numbers."""
          return a * b
      
      
      calculator = StructuredTool.from_function(
          func=multiply,
          name="calculator",
          description="multiply two numbers",
          args_schema=CalculateInput,
          return_direct=True,
          # coroutine= ... <- you can specify an async method if desired as well
      )
      
      print(calculator.invoke({"a": 2, "b": 3}))
      print(calculator.name)
      print(calculator.description)
      print(calculator.args)
      ```
    * **Output**
      ```json
      6
      Calculator
      multiply numbers
      {'a': {'description': 'first number', 'title': 'A', 'type': 'integer'}, 'b': {'description': 'second number', 'title': 'B', 'type': 'integer'}}
      ```
  ### 2. Creating Tools using [`runnables`](../additionals/runnable.md)
  > 

  ### 3. Subclass BaseTool
  > 

## How to create async tools

## How to handing tool errors
> Error handling is must when we are using tools with agents. We have to define proper **error handling strategy**, so that agent can recover from the error and continue the execution.

* A simple strategy is throw a `ToolException` from inside the tool and **must** have to set `handle_tool_error` = `True` by default is it `False` or a string value, or a function otherwise it won't be work. 
* When handler is specified, the exception will catch and the error handling will decides which output have to return from the tool.
* **Examples** 

```python

```

```python 
```

```python 


```