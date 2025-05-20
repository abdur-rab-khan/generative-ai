from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from typing_extensions import Annotated
from typing import List, Optional, Union
from langchain_core.runnables import chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

system = """You are a Quiz Master AI. Your role is to generate engaging, informative, and *unique* quiz questions on any topic provided by the user. You must aim for a variety of question styles, including multiple-choice, true/false, and open-ended questions. Each question must clearly indicate the points awarded for a correct answer. Ensure all questions are clear, concise, and factually accurate. When evaluating user answers, provide a JSON object indicating whether the answer is correct and the points awarded (or 0 if incorrect)."""

example = [
    HumanMessage(
        content="Can you give me a quiz on the topic of programming. and should be in multiple-choice format."
    ),
    AIMessage(
        content="""
        Which keyword is used to define a function in Python? (7 points)
        a) func
        b) define
        c) def
        d) function
        """
    ),
    HumanMessage(
        content="So the answer is: c, In python we use def to create function."
    ),
    AIMessage(
        content="""{{"correct": true, "points": 7}}"""
    ),
    AIMessage(
        content="""
        Which of the following is a valid variable name in Python? (9 points)

        a) 1st_variable
        b) first-variable
        c) first_variable
        d) first variable
        """
    ),
    HumanMessage(
        content="So the answer is: b."
    ),
    AIMessage(
        content="""{{"correct": false, "points": 0}}"""
    ),
    AIMessage(
        content="""
        What is the output of the following code snippet? (5 points)
        ```python
        print(type([]) is list)
        ```
        a) True
        b) False
        c) None
        d) Error
        """
    ),
    HumanMessage(
        content="So the answer is: c."
    ),
    AIMessage(
        content="""{{"correct": false, "points": 0}}"""
    ),
    AIMessage(
        content="""
        What is the time complexity of accessing an element in a list by index in Python? (10 points)
        a) O(1)
        b) O(n)
        c) O(log n)
        d) O(n^2)
        """
    ),
    HumanMessage(
        content="So the answer is: a."
    ),
    AIMessage(
        content="""{{"correct": true, "points": 10}}"""
    ),
    HumanMessage(
        content="Can you give me a quiz on the topic of programming. But the format should be true/false."
    ),
    AIMessage(
        content="""
        True or False: Python is a statically typed language. (5 points)
        """
    ),
    HumanMessage(
        content="So the answer is: False."
    ),
    AIMessage(
        content="""{{"correct": true, "points": 5}}"""
    ),
    AIMessage(
        content="""
        True or False: In Python, a tuple is mutable. (5 points)
        """
    ),
    HumanMessage(
        content="So the answer is: True."
    ),
    AIMessage(
        content="""{{"correct": false, "points": 0}}"""
    ),
]
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=system),
        *example,
        MessagesPlaceholder("topic")
    ]
)

# Initialize llm.
llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)


# Structure output.
class QuestionStructure(BaseModel):
    """
    Structure representing a single quiz question.

    Attributes:
        question (str): The quiz question to be displayed to the user.
        options (Optional[List[str]]): A list of multiple-choice options (if applicable).
        point (int): The number of points assigned to this question.
    """
    question: Annotated[str, ...,
                        "The quiz question to be presented to the user."]
    options: Optional[Annotated[List[str], ...,
                                "List of answer choices, applicable only for multiple-choice questions."]]
    point: Annotated[int, ...,
                     "The number of points assigned to the question."]


class AnswerStructure(BaseModel):
    """
    Structure representing the result of a user's answer.

    Attributes:
        correct (bool): Indicates whether the user's answer was correct.
        earn_point (int): The number of points earned based on the answer.
        correct_answer (str): The correct answer to the question.
    """
    correct: Annotated[bool, ..., "Indicates if the user's answer is correct."]
    earn_point: Annotated[int, ...,
                          "Points earned by the user for this question."]
    correct_answer: Annotated[str, ..., "The correct answer to the question."]


class CombineStructure(BaseModel):
    """
    A unified structure that can represent either a quiz question or an answer evaluation.

    Attributes:
        combine_structure (Union[QuestionStructure, AnswerStructure]):
            Holds either a `QuestionStructure` (representing a quiz question) or 
            an `AnswerStructure` (representing the result of a user's answer).
    """
    combine_structure: Union[QuestionStructure, AnswerStructure]


structured_llm = llm.with_structured_output(CombineStructure)

# Initialize Chains
points = 0
earn_points = 0
topic = None

chat_history = []


def print_quiz(quiz) -> AIMessage:
    global points

    quiz_data = quiz.combine_structure

    if isinstance(quiz_data, QuestionStructure):
        print(f"Question: {quiz_data.question}")
        if quiz_data.options is not None:
            for i, option in enumerate(quiz_data.options):
                print(f"{chr(97 + i)}) {option}")

        points += quiz_data.point
        return AIMessage(content=str(quiz_data))
    else:
        raise Exception("Unexpected structure received:")


def getAnswerFromUser() -> HumanMessage:
    """
    Get answer from the user.
    """
    user_input = input("Enter you answer:- ")
    answer = user_input if user_input else "I don't know."

    human_message = HumanMessage(content=f"So my answer is: {answer}")
    return human_message


def increase_points(result):
    global earn_points

    quiz_result = result.combine_structure

    if isinstance(quiz_result, AnswerStructure):
        earn_points += quiz_result.earn_point
        message = (
            f"Your answer is correct: earn {quiz_result.earn_point} point"
            if quiz_result.correct
            else f"Sorry, Your answer is wrong. correct: {quiz_result.correct_answer}"
        )
        print(message)
    else:
        print("Unexpected structure received: ", quiz_result)


@chain
def quiz_executor(topic):
    llm_with_ps = prompt | structured_llm

    quiz = llm_with_ps.invoke({"topic": [*chat_history, HumanMessage(
        content=f"Give another new question on the topic of {topic} and should be new not duplicate. As the questions increase, the difficulty level should also increase.")]})

    ai_message = print_quiz(quiz)
    human_message = getAnswerFromUser()
    combine_message = [ai_message, human_message]
    chat_history.extend(combine_message)

    quiz_result = structured_llm.invoke(combine_message)
    return quiz_result


while True:
    if (len(chat_history) % 5 == 0 and len(chat_history) != 0):
        isExit = input("Do you want to continues. (y/n) ")
        if isExit == "n" or isExit == "no":
            if points > 0:
                print(f"You earn {earn_points} out of {points}")
            break

    if topic is None:
        user_input = input("Enter you topic name with format:- ")
        topic = user_input if user_input else "random topic any format."

    quiz_result = quiz_executor.invoke(topic)
    increase_points(quiz_result)
