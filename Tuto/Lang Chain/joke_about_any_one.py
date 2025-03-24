import os
import time

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv()


model = ChatOpenAI(model_name="gpt-4o-mini")

prompt_template = """
Tell me joke about {topic}.
Provide me only single joke only.
"""

prompt = PromptTemplate(template=prompt_template,input_variables=["topic"])

if __name__ == "__main__":
    topic_list = ["cat","human","dog"]

    print("\nCHOOSE ANY TOPIC\n")
    print("1. Cat\n2.Human\n3.Dog")

    input_value = int(input("Choose from above: "))

#     Assemble the chain using the pipe operator "|",
    chain = prompt | model

    for chunk in chain.stream({"topic":topic_list[input_value]}):
        print(chunk.content,end="")
        time.sleep(0.1)



