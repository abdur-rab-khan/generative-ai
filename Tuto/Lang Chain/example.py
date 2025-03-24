import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate


model = ChatOpenAI(model_name="gpt-4o-mini")

prompt_template = """
Give the answer in one word: {topic}
"""

prompt = PromptTemplate(
    input_variables=["topic"],
    template=prompt_template
)

chain = prompt | model

if __name__ == "__main__":
    print(chain.invoke({"topic": "what is the capital of france"}).content)