import getpass
import os
import time
from tabnanny import verbose

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent,initialize_agent
from langchain_core.messages import HumanMessage

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together. Input should be two integers separated by commas."""
    print("MULTIPLY FUNCTION IS INVOKED")
    return a * b

@tool
def add(a: int, b: int) -> int:
    """Add two numbers together. Input should be two integers separated by commas."""
    print("ADD FUNCTION IS INVOKED")
    return a + b

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model_name="gpt-4o")


@tool
def magic_function(input: int) -> int:
    """Applies a magic function to an input."""
    print("Magic Function is exceute")
    return input + 2


tools = [magic_function]


query = "what is the value of magic_function(3)?"

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant"),
        ("human", "{input}"),
        # Placeholders fill up a **list** of messages
        ("placeholder", "{agent_scratchpad}"),
    ]
)


agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools,verbose=True)

# print(agent_executor.invoke({"input": query}))

# # STRUCTURED OUTPUT.
# from pydantic import BaseModel, Field
# class ResponseFormatter(BaseModel):
#     """Always use this tool to structure your response to the user."""
#     answer: str = Field(description="The answer to the user's question")
#     followup_question: str = Field(description="A followup question the user could ask")
#
# model_with_tools = model.bind_tools([ResponseFormatter])
#
# print(model_with_tools.invoke("what is the capital of france"))