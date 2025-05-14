# LangChain Expression Language (LCEL)

> LCEL takes directive approach to building new Runnables from existing Runnables.
> The means that you describe what *should* happen, rather than how should happen, allowing LangChain to optimize at run-time.

- We often refer to a **Runnable** created using LCEL as a `"Chain"`. We have to remembers **`Runnable`** is a `"Chain"`.

- [LangChain Expression Language (LCEL)](#langchain-expression-language-lcel)
  - [Benefits of LCEL](#benefits-of-lcel)
  - [Should I use LCEL](#should-i-use-lcel)
  - [Composition Primitives](#composition-primitives)
    - [RunnableSequence](#runnablesequence)
    - [RunnableParallel](#runnableparallel)
  - [Composition Syntax](#composition-syntax)
  - [Legacy chains](#legacy-chains)

## Benefits of LCEL

- LangChain optimize the run-time execution of chains built with LCEL in a number of ways:
    1. **Optimized Parallel execution:**
        - Parallel execution using **LCEL** can reduce the execution time, latency by processing in parallel instead of sequently. Using [`RunnableParallel`](#runnableparallel) to run in parallel or run multiple inputs through [`Runnable Batch API`]().
    2. **Guaranteed Async support**
        - LCEL Chains can be run asynchronously using [Runnable Async API](). This is useful when you are in server environment where you want to handle large number of request concurrently.
    3. **Simplify streaming**
        - LCEL Chains can be streamed, allowing for incremental output as the chain is executed.

- Other benefits includes
    1. **Seamless tracing with LangSmith**
        - As the chain become complex and more complex, To trace what happen at every step, We can use LangSmith. It will automatically trace it.
    2. **Standard API:**
        - Chains can be easily handled, because all chains are build using Runnable Interface.
    3. **Deployable with LangServe:**
        - Chains build with LCEL can easily deployed using LangServe for making available for public.

## Should I use LCEL

- As application become larger and larger with hundred of steps in products, you need a structured way to manage how data flows between those components. In this situation `LCEL` came in the picture.
- We application require complex state management, branching, cycles or multiple agents, best approach is to use [LangGraph](../../Lang%20Graph/01_langchain_glossary/).
- In LangGraph, we define graphs that specify the flow of the application. Using `LCEL` in each individual nodes when needed can make more readable and maintainable.

- Some Impotent Note.
  1. LCEL is not for simple LLM call you don't need this.
  2. If have chain similar to this ( prompt + llm + output parser ) you can use LCEL.
  3. If you're building complex chain using LangGraph instead of LangChain.

## Composition Primitives

- Chains are build by composing existing **`Runnables`** together. There are two main composing primitives [RunnableSequence](#runnablesequence), [RunnableParallel](#runnableparallel).
- You can see list of primitive from [here](https://python.langchain.com/api_reference/core/runnables.html).

### RunnableSequence

> RunnableSequence is a composing primitives that allows us to **`"Chain"`** multiple runnables sequentially, where the output of one runnable server as input to next.

- **Example**

    ```py
    from langchain_core.runnables import RunnableSequence, RunnableLambda
    
    
    addition = RunnableLambda(lambda x: x + 10)
    multiplication = RunnableLambda(lambda x: x * 2)
    
    chain = RunnableSequence(addition, multiplication)
    
    chain.invoke(10)
    ```

  - **Output**

    ```shell
    40
    ```

- **It is similar to this**

    ```py
    from langchain_core.runnables import RunnableSequence, RunnableLambda
    
    
    addition = RunnableLambda(lambda x: x + 10)
    multiplication = RunnableLambda(lambda x: x * 2)

    add = addition.invoke(10)
    multi = multiplication(add)

    print(multi)
    ```

  - **Output**

    ```shell
    40
    ```

### RunnableParallel

> RunnableParallel is compositing primitive that allows us to run multiple runnables concurrently, with the same input to each.

- **Example**
  
  ```py
  from langchain_core.runnables import RunnableParallel, RunnableLambda

  addition = RunnableLambda(lambda x: x + 10)
  multiplication = RunnableLambda(lambda x: x * 2)
  
  chain = RunnableParallel({
      "add": addition,
      "mul": multiplication
  })
  
  chain.invoke(10)
  ```

  - **Output**

    ```shell
    {'add': 20, 'mul': 20}
    ```

- For synchronous parallel execution it use **`ThreadPoolExecutor`**.
- For asynchronous parallel execution it use **`async.gather`**.

## Composition Syntax

> So in LangChain, We have some shorthand technique to use **`RunnableSequence`** or **RunnableParallel** that make code more readable.

- To implement this we use **operator overloading** to overload the behavior of operator or build-in methods. such as **`|`** or **`RunnableSequence`**.

---

1. **The | Operator**

   - We overloaded **bit-wise or** operator to create RunnableSequence from two runnables.

   - **Example**

    ```py
    # We know that both prompt and llm are build using runnable interface
    
    chain = prompt | llm
  
    chain.invoke({"input": [HumanMessage(content="what is the capital of india")]})
    ```

1. **The .pipe method**

- **Example**
  
  ```py
  chain = prompt.pipe(llm)

  chain.invoke({"input": [HumanMessage(content="what is the capital of india")]})
  ```

- For more see from [here](./langchain_expression_language.ipynb/#examples-of-lcel).
