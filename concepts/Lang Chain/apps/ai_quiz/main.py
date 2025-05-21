from prompt import prompt
from structure import CombineStructure
from utils import check_result, print_quiz, getAnswerFromUser

from langchain_openai import ChatOpenAI
from langchain_core.runnables import chain
from langchain_core.messages import HumanMessage

# Initialize llm with structure.
llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)
structured_llm = llm.with_structured_output(CombineStructure)

# Initialize Chains
points = 0
earn_points = 0
topic = None
chat_history = []


@chain
def quiz_executor(topic):
    llm_with_ps = prompt | structured_llm

    quiz = llm_with_ps.invoke({"topic": [*chat_history, HumanMessage(
        content=f"Give another new question on the topic of {topic} and should be new not duplicate. As the questions increase, the difficulty level should also increase.")]})

    ai_message = print_quiz(points, quiz)
    human_message = getAnswerFromUser()
    combine_message = [ai_message, human_message]
    chat_history.extend(combine_message)

    quiz_result = structured_llm.invoke(combine_message)
    return quiz_result


if __name__ == "__main__":
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
        check_result(earn_points, quiz_result)
