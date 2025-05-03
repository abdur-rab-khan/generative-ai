# Few-Shot Prompting

There are few techniques to improve model performance, **Few-Shot Prompting** is one of them. In **Few-Shot Prompting** we give example input with excepted output to the model prompt. The technique is based up [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) paper.

- [Few-Shot Prompting](#few-shot-prompting)
  - [1. Generate Examples](#1-generate-examples)
  - [2. Numbers Examples](#2-numbers-examples)
  - [3. Selecting Examples](#3-selecting-examples)
  - [4. Formatting Examples](#4-formatting-examples)

## 1. Generate Examples

- The first and most important step of few-shot prompting is a good dataset of examples. Good examples should be relevant at **runtime**, **clear**, **informative**, and **provided information** that was not already know to the model.

- Basic way to generating examples are:
    1. Manual: Should be written by the person/people.
    2. Better model: A better model's response are used as example for a worse(cheaper) model
    3. User feedback: Users leave feedback on interaction with application and example are generated based on feedback can be turn examples.
    4. LLM feedback: Same as user feedback but the process is automated by having models evaluates themselves.

- Which approach is best it is depends on your task.
  - For small you can create valuable hand-craft few example can be best.
  - And For task where corrected is priority than useful is to generate more example by using automation can be best.

- Single turn vs Multi turn
  - In **Single turn** we just have user input and expected output.
  - In **Multi turn**, We have complex type of example, the entire conversation where model initially response incorrectly and user than tells the model how to correct its answer.

## 2. Numbers Examples

- Once we have set of good examples. the critical moment is to think about how many example is should be in each prompt.
- The more example generally consider as better, but larger prompts can increase cost and latency.
- Beyond the threshold having too many examples can confuse the model.
- Finding the right numbers of examples is totally depends on the model, the task, the quality of the examples.
- The better the model is the fewer examples its need to performs well and the more quickly you hit steeply diminishing returns on adding more examples.
- The best/only way is to run experiments with different number of examples

## 3. Selecting Examples

- Assume we are not adding entire example dataset into prompt, we need to have a way of selecting examples from our dataset on a give input
- We do this:
  1. Randomly
  2. By (**semantic**, **keyword-based**) similar of the inputs.
  3. Based on some other constraints, like token size.

  - The LangChain has number of [`ExampleSelectors`](https://python.langchain.com/docs/how_to/#example-selectors) which make it easy to use any of these techniques.
  - Selecting by semantic similarity leads to the best model performance.But how important this is, is again model and task specific, and is something worth experimenting with.

## 4. Formatting Examples

- There are some basic options to add insert examples.
  - In the system prompt as a string
  - As their own message

- If we insert example into the [`SystemMessage`](../02_messages/messages.md/#1-systemmessage) as a string. we'll need to make sure it's clear to the model which part are the input versus output.
- If we insert examples as message, where each message represent a sequence [`HumanMessage`](../02_messages/messages.md/#2-humanmessage), [`AIMessage`](../02_messages/messages.md/#3-aimessage). we might want to assign name into the message like `example_user` or `example_assistance` to make it clear that these message corresponds to different actors then the latest input message.
- **Formatting tool call examples**
  - One area where formatting examples as messages, can be tricky is when our example is tool calls. This is because different models have different sequence constraints which types of message sequences are allowed when any tool call are generated.
    - Some model requires that any `AIMessage` with tool calls be immediately followed by `ToolMessages` for every tool call.
    - Some model requires that any `ToolMessage` be immediately followed by `AIMessage` for every tool call.
    - Some models require that tools are passed into the model if there are any tool call / ToolMessage in the chat history.

- These requirements totally depends upon the model we are using so first we have to check it how model behave with tools.
- Based on tool call schema you have to follow on the set of examples.
- you can try adding dummy ToolMessages / AIMessages to the end of each example with generic contents to satisfy the API constraints.

- [How to use few shot prompting](./few_shot_prompting.ipynb/#example-1)
