# Runnable Interface

> The runnable interface is the foundation for working with LangChain Components, and it's implemented across many of them such as **`chat model`**, **`output parser`**, **`retrievers`**, **`complied LangGraph graphs`** and many more.

- [Runnable Interface](#runnable-interface)
  - [Overview of Runnable Interface](#overview-of-runnable-interface)
    - [1. Invoked](#1-invoked)
    - [2. Batched](#2-batched)
    - [3. Streamed](#3-streamed)
  - [Optimized parallel execution (batch)](#optimized-parallel-execution-batch)
  - [Asynchronous Support](#asynchronous-support)
  - [Streaming API's](#streaming-apis)
  - [Input and Output types](#input-and-output-types)
  - [Inspecting Schemas](#inspecting-schemas)
  - [Runnable Configuration](#runnable-configuration)
  - [Propagation of **`RunnableConfig`**](#propagation-of-runnableconfig)
  - [Creating a runnable from a function](#creating-a-runnable-from-a-function)

## Overview of Runnable Interface

- It provide standard interface that allow runnable component to be:
    1. **`invoked`**: A single input is transformed into an output.
    2. **`Batched`**: Multiple inputs are efficiently transformed into output.
    3. **`Streamed`**: Output are streamed as they are produced
    4. **`Inspect`**: Access Schematic information about input, output, configuration
    5. **`Composed`**: Multiple runnable can be composed together using [langchain expression language](../additionals/langchain_expression_language.md) to create complex pipeline.

### 1. Invoked

```py
from langchain_core.runnable import RunnableLambda

runnable = RunnableLambda(lambda x: str(x))

runnable.invoke(4) # '4'
# ainvoke --> for async
```

### 2. Batched

```py
from langchain_core.runnable import RunnableLambda

runnable = RunnableLambda(lambda x: str(x))

runnable.batched([1,2,3,4]) # ['1','2','3','4']
# abatched --> for async
```

### 3. Streamed

```py
from langchain_core.runnables import RunnableLambda


def func(x):
        for y in x:
                yield str(y)


runnable = RunnableLambda(func)

for chunk in runnable.stream(range(5)):
        print(chunk)

# async for chunk in await runnable.astream(range(5)):
#     print(chunk)
```

---

## Optimized parallel execution (batch)

- LangChain Runnable provided build-in API's to process multiple inputs in parallel that improve performance significantly:
        1. **`batch`**: Process multiple inputs in parallel, return outputs in same order as the inputs.
        2. **`batch_as_completed`**: Same as previous one, but result value as they completed it can be out of order.

- **Note**: The implementation of **`batch`** and **`batch_as_completed`** use **thread** tool executor to run in parallel.

## Asynchronous Support

- LangChain Runnables also support asynchronous
  - It can be call using `await` syntax in Python.
  - All synchronous runnables methods are start with prefix **"a"**
    - eg. (**`ainvoke`**, **`abatch`**, **`astream`**, **`abatch_as_completed`**).

  - For more refer [asynchronous programming in LangChain](../additionals/async.ipynb).

## Streaming API's

Streaming is critical in application based on LLM feel responsive to end user.

- Runnables Provides three API's for streaming
        1. sync ➡️ **`stream`**, async ➡️ **`astream`**: yields the output.
        2. The async ➡️ **`astream_events`**: A more advanced API allowing as to stream from intermediate to final step.

## Input and Output types

Every **`Runnables`** are characterized by an input and output types (It can be python object and defined by runnable).

- Runnable methods works with these input/output types:
  - invoke: Accepts an input and return output
  - batch: Accepts list of inputs and return list of outputs
  - stream: Accepts input and return a generator that yields outputs

- The input type and output type vary by component:

| Component | Input Type | Output Type |
|-----------|------------|-------------|
| Prompt | dictionary | PromptValue |
| ChatModel | a string, list of chat messages or a PromptValue | ChatMessage |
| LLM | a string, list of chat messages or a PromptValue | String |
| OutputParser | the output of an LLM or ChatModel | Depends on the parser |
| Retriever | a string | List of Documents |
| Tool | a string or dictionary, depending on the tool | Depends on the tool |

## [Inspecting Schemas](https://python.langchain.com/docs/concepts/runnables/#inspecting-schemas)

## Runnable Configuration

- Runnable methods that are use to invoke accept second arguments called **`RunnableConfig`**.
  - It can be dictionary containing configuration that are used at run time during the execution.

- A **`RunnableConfig`** can have any of the following properties defined:

| Attribute | Description |
|-----------|-------------|
| run_name | Name used for the given Runnable (not inherited). |
| run_id | Unique identifier for this call. sub-calls will get their own unique run ids. |
| tags | Tags for this call and any sub-calls. |
| metadata | Metadata for this call and any sub-calls. |
| callbacks | Callbacks for this call and any sub-calls. |
| max_concurrency | Maximum number of parallel calls to make (e.g., used by batch). |
| recursion_limit | Maximum number of times a call can recurse (e.g., used by Runnables that return Runnables) |
| configurable | Runtime values for configurable attributes of the Runnable. |

- **Example**

    ```py
    some_runnable.invoke(
    some_input, 
    config={
      'run_name': 'my_run', 
      'tags': ['tag1', 'tag2'], 
      'metadata': {'key': 'value'}
      
    })
    ```

## Propagation of **`RunnableConfig`**

- Many **`runnables`** can be composed by other runnables
  - **`RunnableConfig`** can propagate to all sub-calls made by the Runnables.
  - Providing run-time configuration values to the parent Runnable that are inherited by all sub-calls.
  - If this is not happen, It is impossible to set and propagate callbacks or other configuration values like **`tags`** and **`metadata`**.

- There are two main pattern by which new **`Runnable`** created:
  - Declarative using [LangChain Expression Language](../additionals/langchain_expression_language.md).

    ```py
    chain = prompt | chat_model | output_parser
    ```

  - Using a custom runnable

    ```py
    def foo(input):
        # Note that .invoke() is used directly here
        return bar_runnable.invoke(input)
    foo_runnable = RunnableLambda(foo)
    ```

## Creating a runnable from a function

- We may need to create custom runnable for arbitrary logic.
- This is especially useful if using [LCEL](../additionals/langchain_expression_language.md) to compose multiple Runnables.
- We may need to create custom processing logic in one of the step.

- There are two way to create custom Runnable from a function.
  1. **`RunnableLambda`**: Use this for simple transformations where streaming is not required.
  2. **`RunnableGenerator`**: use this for more complex transformations when streaming is needed.