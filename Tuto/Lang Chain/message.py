import time

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

load_dotenv()

llm = ChatOpenAI(model_name="gpt-4", temperature=0.3)  # Corrected model name

messages = [
    SystemMessage(content="You're a maths teacher who can solve maths problems in simple and easy-to-understand words. Use some Hinglish words."),
    HumanMessage(content="What is 2 + 2?"),
    AIMessage(content="Sure beta, this is a simple problem. The answer to 2 + 2 is 4."),
]

# Main execution
if __name__ == "__main__":
    question = input("Enter you Questions::- ")
    messages.append(HumanMessage(content=question))

    for chunk in llm.stream(messages):
        print(chunk.content,end="")
        time.sleep(0.05)