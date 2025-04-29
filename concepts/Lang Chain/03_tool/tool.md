# ⚒️ Tools in LangChain
>
> In LangChain Tools are simple Python **function** with a **schema** that defines function **name**, **description** and **expected args**. Tools can be passed to [chat model](../01_chat_model/chat_model.md) that support [tool calling](./tool_calling.md) allowing the model to request the execution of function with specific output.

- [⚒️ Tools in LangChain](#️-tools-in-langchain)
  - [Key Concept](#key-concept)
  - [Tool Interface](#tool-interface)
  - [How to create tools](#how-to-create-tools)
  - [1. Create tools using function](#1-create-tools-using-function)
  - [2. Creating Tools using `runnables`](#2-creating-tools-using-runnables)
  - [3. Subclass BaseTool](#3-subclass-basetool)
  - [Tool artifacts](#tool-artifacts)
  - [Special type annotations](#special-type-annotations)
  - [Best practices](#best-practices)
  - [How to create async tools](#how-to-create-async-tools)
  - [How to handing tool errors](#how-to-handing-tool-errors)

## Key Concept

- Tools are a way to encapsulate a function and its schema so that it can be passed to a chat model.
- Tools are created using the @tool decorator, supporting the following features:
  1. The chat model automatically infers the tool’s name, description, and expected arguments, while also supporting customization.
  2. Tools can be defined to return artifacts (e.g., images, dataframes, etc.).
  3. Input arguments can be hidden from the schema by using injected tool arguments.

## Tool Interface

- The tool interface are defined in the [BaseTool](https://python.langchain.com/api_reference/core/tools/langchain_core.tools.base.BaseTool.html#langchain_core.tools.base.BaseTool) class. which is the subclass of the [Runnable Interface](../additionals/runnable.md)

- The key attribute corresponding to tool's **schema**.
    1. **name**: The name of the Tool
    2. **description**: A Description about of what actually they do.
    3. **args**: Properties that return JSON schema for the tool's args. Optional but required to provide more information or validation.
    4. **return_direct**: Only relevant for agents. if `return_direct` is **True**. it will stop after invoking and return the result directly to the user.

- The key method to execute the function associated to tool
  1. invoke: Invoke the tool with the given args.
  2. ainvoke: Invokes the tools with given args but **asynchronously**. using [async programming in LangChain](../additionals/async.ipynb)

## How to create tools

- LangChain supports the creation of tools from:
    1. [Functions](#1-create-tools-using-function)
    2. [LangChain Runnables](#2-creating-tools-using-runnables)
    3. [By sub-class from `BaseTool`](#3-subclass-basetool) -- This is most flexible and customizable method to create tool.

## 1. Create tools using function

- The recommended way to create a tool is using [`@tool`](https://python.langchain.com/api_reference/core/tools/langchain_core.tools.convert.tool.html) decorator. The decorator is design to simply the creation and should be used in most cases.

  - [How to create tools](https://python.langchain.com/docs/how_to/custom_tools/)
    > Tool are commonly use in constructing `agents`, you will need to provide list of `tools`.

  - There are two way to create tools using functions
    1. [Using `@tool` decorators](#1-tool)
    2. [Using `StructureTool`](#2-structuredtool)

    ### 1. `@tool`

      > This `@tool` is the simples way to define a custom **tool**.The decorator uses the function name as the tool name by default, but this can be overridden by passing a string as the first argument. Additionally, the decorator will use the function's docstring as the tool's description - so a docstring MUST be provided.
  
    - **Examples**
  
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
  
      - **Note** that `@tool` also supports parsing of [`Annotated`](../additionals/annotated.ipynb), nested schema, and other features.
  
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
  
      - Also we can **customize** **tool name** and JSON args by passing them into the tool decorator
  
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
  
      - **Docstring parsing**
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
  
        - Output

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
  
    ### 2. StructuredTool
  
      > `StructuredTool.from_function` class method provide bit more configurability than `@tool` decorator with many complex code.
  
    - **Examples**

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

    - [**API Reference**](https://python.langchain.com/api_reference/core/tools/langchain_core.tools.structured.StructuredTool.html)
  
    - To configure it:
  
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

    - **Output**
  
        ```json
        6
        Calculator
        multiply numbers
        {'a': {'description': 'first number', 'title': 'A', 'type': 'integer'}, 'b': {'description': 'second number', 'title': 'B', 'type': 'integer'}}
        ```

## 2. Creating Tools using [`runnables`](../additionals/runnable.md)

## 3. Subclass BaseTool
  
  > You can define custom tool by sub-classing from `BaseTool`. This providers maximum control over the tool definition, but require writing more codes.

- **Example**

    ```python
    from typing import Optional
    from langchain_core.callbacks import (
        AsyncCallbackManagerForToolRun, CallbackManagerForToolRun)
    from langchain_core.tools import BaseTool
    from langchain_core.tools.base import ArgsSchema
    from pydantic import Field, BaseModel
    
    
    class CalculatorInput(BaseModel):
        a: int = Field(description="first number")
        a: int = Field(description="second number")
    
    # Note: It's important that every field has type hints. BaseTool is a Pydantic class and not having type hints can lead unexpected behavior.
    
    
    class CustomCalculatorTool(BaseTool):
        name: str = "calculator"
        description: str = "useful for when you need to solve math problems."
        args_schema: Optional[ArgsSchema] = CalculatorInput
        return_direct: bool = True
    
        def _run(self, a: int, b: int, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
            """Use the tool"""
            return a * b
    
        async def _arun(self, a: int, b: int, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
            """Use the tool asynchronously"""
    
            return self._run(a, b, run_manager=run_manager.get_sync())
    
    
    multiply = CustomCalculatorTool()
    print(multiply.name)
    print(multiply.description)
    print(multiply.args)
    print(multiply.return_direct)
    
    print(multiply.invoke({"a": 2, "b": 3}))
    print(await multiply.ainvoke({"a": 2, "b": 3}))
    ```

## Tool artifacts

## Special type annotations

## Best practices

## How to create async tools

> LangChain tools are build using [Runnable Interface](../additionals/runnable.md), All runnable expose `invoke` and `ainvoke` method (as well as `batch`, `abatch`, `stream`, `astream` ect).

- So even if you implementation of a tool is `sync`. you could still able to use `ainvoke` interface, but there are some important things you have to know:
  1. LangChain's by default provide `async` implementation that assume function is expensive to compute. so it'll try to delegate execution to another thread.
  2. If you're code base is `async` you should have to create `async` tool rather then `sync`.
  3. If you need both `sync` and `async` implementation you can use `StructuredTool.from_function` or sub-class from `BaseTool`.
  4. If implementing both sync and async, and the sync code is fast to run, override the default LangChain async implementation and simply call the sync code.
  5. You CANNOT and SHOULD NOT use the sync invoke with an async tool.

- **Example**
  
  ```python
  from langchain_core.tools import StructuredTool

  def multiply(a:int,b:int)->int:
    """Multiply two numbers"""

    return a * b


  calculator_tool = StructuredTool.from_function(func=multiply)

  print(calculator.invoke({"a": 2, "b": 3}))
  print(
    await calculator.ainvoke({"a": 2, "b": 5})
  )  # Uses default LangChain async implementation incurs small overhead
  ````

  ```python
  from langchain_core.tools import StructuredTool


  def multiply(a: int, b: int) -> int:
      """Multiply two numbers."""
      return a * b
  
  
  async def amultiply(a: int, b: int) -> int:
      """Multiply two numbers."""
      return a * b
  
  
  calculator = StructuredTool.from_function(func=multiply, coroutine=amultiply)
  
  print(calculator.invoke({"a": 2, "b": 3}))
  print(
      await calculator.ainvoke({"a": 2, "b": 5})
  )  # Uses use provided amultiply without additional overhead
  ```

  - You should not and cannot use .invoke when providing only an async definition.

  ```python
  @tool
  async def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


  try:
      multiply.invoke({"a": 2, "b": 3})
  except NotImplementedError:
      print("Raised not implemented error. You should not be doing this.")
  ```

  - **Output**
  
    ```shell
    Raised not implemented error. You should not be doing this.
    ```

## How to handing tool errors

> Error handling is must when we are using tools with agents. We have to define proper **error handling strategy**, so that agent can recover from the error and continue the execution.

- A simple strategy is throw a `ToolException` from inside the tool and **must** have to set `handle_tool_error` = `True` by default is it `False` or a string value, or a function otherwise it won't be work.
- When handler is specified, the exception will catch and the error handling will decides which output have to return from the tool.
- **Examples**

  ```python
  from langchain_core.tools import ToolException, StructuredTool
  
  def getWeather(city:str) -> int:
    """Get the weather of city"""
    raise ToolException(f"Error: There is no city found with this name {city}")

  get_weather_tool = StructuredTool.from_function(
    func=get_weather,
    handle_tool_error=True,
  )
  
  get_weather_tool.invoke({"city": "foobar"})
  ```

  - **Output**

    ```shell
    'Error: There is no city by the name of foobar.'    
    ```

  - **Example with default string**
    - So we can directly specify a message string instead of writing `True`, When error will happen than that string will show instead of ToolException message.

    ```python
    from langchain_core.tools import ToolException, StructuredTool
  
    def getWeather(city: str) -> int:
      """Get the weather of the city"""
      raise ToolException()
  
    get_weather_tool = StructuredTool.from_function(
      func=getWeather,
      handle_tool_error="There is no such city, but it's probably above 0K there!"
    )
  
    get_weather_tool.invoke({"city":"foobar"})
    ```
  
    - **Output**
  
      ```shell
      There is no such city, but it's probably above 0K there!
      ```

  - **Example with custom function**

    ```python
    from langchain_core.tools import ToolException, StructuredTool

    def error_handing(err:ToolException)-> str:
      return f"The following errors occurred during tool execution: `{error.args[0]}`"

    def getWeather(city:str) -> int:
      """Get the weather of the city"""

      raise ToolException(f"Error: There is no city found with this name {city}")

    get_weather_tool = StructuredTool.from_function(
      func=getWeather,
      handle_tool_error =error_handing
    )

    get_weather_tool.invoke({"city":"foobar"})
    ```

    - **Output**

      ```shell
      'The following errors occurred during tool execution: `Error: There is no city by the name of foobar`'
      ```
