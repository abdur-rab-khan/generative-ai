# Few-Shot Prompting

There are few techniques to improve model performance, **Few-Shot Prompting** is one of them. In **Few-Shot Prompting** we give example input with excepted output to the model prompt. The technique is based up [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) paper.

- There are following things we have to keep in mind when doing [few-shot prompting](#few-shot-prompting)
  1. [How are examples generated?](#1-generate-examples)
  2. [How many examples are in each prompt?](#2-numbers-examples)
  3. [How are examples selected at runtime?](#3-selecting-examples)
  4. [How are examples are formatted in the prompt?](#4-formatting-examples)

## 1. Generate Examples

> The first and most important step of few-shot prompting is a good dataset of examples. Good examples should be relevant at **runtime**, **clear**, **informative**, and **provided information** that was not already know to the model.

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

- Once we have set of good examples. the critical moment is to think about many example is should be in each prompt.
- The more example generally consider as better, but larger prompts can increase cost and latency.
- Beyond the threshold having too many examples can confuse the model.
- Finding the right numbers of examples is totally depends on the model, the task, the quality of the examples.
- The better the model is the fewer examples its need to performs well and the more quickly you hit steeply diminishing returns on adding more examples.
- The best/only way is to run experiments with different number of examples


## 3. Selecting Examples

## 4. Formatting Examples
