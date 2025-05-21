from pydantic import BaseModel
from typing_extensions import Annotated
from typing import Optional, List, Union


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
