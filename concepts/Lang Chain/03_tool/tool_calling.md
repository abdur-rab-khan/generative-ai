# Tool calling in LangChain

> Many AI Applications interact with humans directly. It is must for model to response in a natural language that human can understand. But what about cases where we want a model to also directly interact with ***system***, such as **Databases**, or an **API**. To interact with these systems we have to use ***API's*** with required payload **structure**. For this kind of mechanism we use [tool calling](https://platform.openai.com/docs/guides/function-calling/example-use-cases?api-mode=responses).

- [Tool calling in LangChain](#tool-calling-in-langchain)
  - [Key concepts](#key-concepts)
    - [Tool binding](#tool-binding)
    - [Tool calling](#tool-calling)
      - [**Pass tool output to chat models**](#pass-tool-output-to-chat-models)
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
    3. [Tool calling](#tool-calling)
        - The model decides to call the tool its response follow to the tool's input schema.
    4. [Tool Execution](#tool-execution)
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

  - `bind_tools(list_tools)` `bind_tools` accepts only tools in the form of list `[tool_1,tool_2...]`.

### Tool calling

> A key principle of tools calling is model decides when to use a tool based on input's relevance. the model doesn't need to call tool always. For example unrelated input, the model would not call tools.

- ***💀 Note*** : Important things we have to note, model can only ***decides*** or generate the ***arguments*** for a tool. it is not able to execute the tools.

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

  - **Using ChatModel to call tools**
  > Tool calling is general technique that generates structured output from a model. and use that output to invoke a tool.

    ![tool-calling-by-chat-model](https://python.langchain.com/assets/images/tool_call-8d4a8b18e90cacd03f62e94071eceace.png)

  - [Models that supports tool calling](https://python.langchain.com/docs/integrations/chat/#featured-providers)
  
    - **Example of tool calling using chat model**

      ```python
      from langchain_core.tools import tool
      from langchain_openai import ChatOpenAI
      from pydantic import BaseModel, Field
      
      
      class InputSchema(BaseModel):
          a: int = Field(description="first number")
          b: int = Field(description="second number")
      
      
      @tool(args_schema=InputSchema)
      def multiply(a: int, b: int):
          """Multiply two numbers"""
      
          return a * b
  
      llm = ChatOpenAI(model="gpt-4o-mini")
      
      llm_with_tools = llm.bind_tools([multiply])
      
      query = "what is 2 multiply by 5."
      
      print(llm_with_tools.invoke(query))
      ```  
  
    - **Output**
  
        ```python
        AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_iXj4DiW1p7WLjTAQMRO0jxMs', 'function': {'arguments': '{"a":3,"b":12}', 'name': 'multiply'}, 'type': 'function'}], 'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 17, 'prompt_tokens': 80, 'total_tokens': 97}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_483d39d857', 'finish_reason': 'tool_calls', 'logprobs': None}, id='run-0b620986-3f62-4df7-9ba3-4595089f9ad4-0', tool_calls=[{'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_iXj4DiW1p7WLjTAQMRO0jxMs', 'type': 'tool_call'}], usage_metadata={'input_tokens': 80, 'output_tokens': 17, 'total_tokens': 97})
        ```
  
      - Above We have `tool_calls` dicts that includes **tool name**, **dict of arguments** and optionally id.
  
          ```json
          [
            {
              "name": 'multiply',
              "args": {
                  "a": 2,
                  "b": 5
                },
            "id": 'call_YVqEZ9bvbIGndQYu484Fv3O6',
            "type": 'tool_call'
          }
        ]
         ```

      - The `tool_calls` attribute should contain valid tool calls. But something can output be a malformed tool calls (e.g arguments does not have valid schema).
      - In such cases instance of [`InvalidToolCall`](https://python.langchain.com/api_reference/core/messages/langchain_core.messages.tool.InvalidToolCall.html#langchain_core.messages.tool.InvalidToolCall) are populated in the `.invalid_tool_calls` attribute. An `InvalidToolCall` contains name, string arguments, identifiers and error message.
      - ***💀 Note*** : We have to keep in mind these things for better error handling.

  - As we see there llm generate argument to a tool, You can see at the docs for [`bind_tools()`](https://python.langchain.com/api_reference/openai/chat_models/langchain_openai.chat_models.base.BaseChatOpenAI.html#langchain_openai.chat_models.base.BaseChatOpenAI.bind_tools) to learn about all the way to customize how you LLM select tools, as well as [guide how to force llm to call a tool](https://python.langchain.com/docs/how_to/tool_choice/) rather than letting it decides.

#### **Pass tool output to chat models**

![pass-tool-output-to-chat-models](https://python.langchain.com/assets/images/tool_invocation-7f277888701ee431a17607f1a035c080.png)

![pass-tool-output-to-chat-models](https://python.langchain.com/assets/images/tool_results-71b4b90f33a56563c102d91e7821a993.png)

- **Example**

  ```py
  from langchain_core.messages import HumanMessage

  llm_with_tools = llm.bind_tools([...tools])

  query = "what is 3 * 2? Also, what is 11 + 49"
  messages = [HumanMessage(content=query)]

  ai_message = llm_with_tools.invoke(messages)

  print(ai_message)

  messages.append(ai_message)
  ```

  - **Output**

    ```shell
    [{'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_GPGPE943GORirhIAYnWv00rK', 'type': 'tool_call'}, {'name': 'add', 'args': {'a': 11, 'b': 49}, 'id': 'call_dm8o64ZrY3WFZHAvCh1bEJ6i', 'type': 'tool_call'}]
    ```

  - So if we invoke LangChain `Tool` with a `ToolCall`. we'll automatically get back a [`ToolMessage`](../02_messages/messages.md/#5-toolmessage) that can be fed back to the model by pushing into the messages list.

    ```py
    for tool_call in ai_message.tool_calls:
      select_tool = tool_by_name[tool_call["name"]]
      tool_msg = select_tool.invoke(tool_call)
      messages.append(tool_msg)
  
    print(messages)
    ```

    - **Output**

      ```py
      [
        HumanMessage(content='what is 3 * 2? Also, what is 11 + 49', additional_kwargs={}, response_metadata={}), 
        AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_n7dPtZmrw7IsD0aShBwKRhRH', 'function': {'arguments': '{"a": 3, "b": 2}', 'name': 'multiply'}, 'type': 'function'}, {'id': 'call_WtoOMhOAwKdvfga0jMFeyncd', 'function': {'arguments': '{"a": 11, "b": 49}', 'name': 'add'}, 'type': 'function'}], 'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 51, 'prompt_tokens': 96, 'total_tokens': 147, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_129a36352a', 'finish_reason': 'tool_calls', 'logprobs': None}, id='run-37d38044-dda7-44af-8362-1da3fabf2fd7-0', tool_calls=[{'name': 'multiply', 'args': {'a': 3, 'b': 2}, 'id': 'call_n7dPtZmrw7IsD0aShBwKRhRH', 'type': 'tool_call'}, {'name': 'add', 'args': {'a': 11, 'b': 49}, 'id': 'call_WtoOMhOAwKdvfga0jMFeyncd', 'type': 'tool_call'}], usage_metadata={'input_tokens': 96, 'output_tokens': 51, 'total_tokens': 147, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}), 
        ToolMessage(content='6', name='multiply', tool_call_id='call_n7dPtZmrw7IsD0aShBwKRhRH'), 
        ToolMessage(content='60', name='add', tool_call_id='call_WtoOMhOAwKdvfga0jMFeyncd')
      ]
      ```

    - And finally, we'll invoke the model, model with decide the result based on given information.

      ```py
      llm_with_tools.invoke(messages)
      ```

    - **Output**

      ```shell
      AIMessage(content='The result of \\(3 \\times 2\\) is \\(6\\), and \\(11 + 49\\) equals \\(60\\).', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 31, 'prompt_tokens': 162, 'total_tokens': 193, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_129a36352a', 'finish_reason': 'stop', 'logprobs': None}, id='run-831e1509-dc9b-4ebf-bfaf-f9d825281c2c-0', usage_metadata={'input_tokens': 162, 'output_tokens': 31, 'total_tokens': 193, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})
      ```

    - **Note** : Each [`tool_message`](../02_messages/messages.md/#5-toolmessage) must includes `tool_call_id` that is exact same `id` that is original tool calls that is generated by the model. This helps the model match tool response with tool calls.

    - Tool calling agents, like those in [LangGraph](../../Lang%20Graph/02_agentic_patterns/), use this basic flow to answer queries and solve tasks.

  - **Parsing**
  
  > After getting desired output, [output parsers](https://python.langchain.com/docs/how_to/#output-parsers) can further process the output. For example can convert the `tool_calls` values into Pydantic objects using the [`PydanticToolsParser`](https://python.langchain.com/api_reference/core/output_parsers/langchain_core.output_parsers.openai_tools.PydanticToolsParser.html).

### Tool Execution

> Tools are implement on the runnable interface, which means that they can be invoked e.g `tool.invoke(args)`, `tool.ainvoke(args)` (for asynchronous).

## Best practices

- When designing a tool used by the model, keep the following in mind:
  
  1. Tools are should be well named, correctly-documented and properly type-hinted are make easier for the model.
  2. Design simple and narrowly scoped (very specific task), as they are easier for the model to use.
  3. Use chat models that support [tool calling](./tool_calling.md)
