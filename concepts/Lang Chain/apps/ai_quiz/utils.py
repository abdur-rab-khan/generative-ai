from structure import QuestionStructure, AnswerStructure

from langchain_core.messages import AIMessage, HumanMessage


def print_quiz(points: int, quiz) -> AIMessage:
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


def check_result(earn_points: int, result):
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
