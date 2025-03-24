from tabnanny import verbose
import time

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, AgentExecutor,create_openai_tools_agent,create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage

load_dotenv()


# Tools

@tool
def multiplication(a: int, b: int) -> int:
    """Multiplication function that take two arguments and return the multiplication of them"""
    print("MULTIPLICATION FUNCTION IS CALLED")
    return a * b


@tool
def addition(a: int, b: int) -> int:
    """Addition function that take two arguments and return the addition of them"""
    print("ADDITION FUNCTION IS CALLED")
    return a + b


@tool
def subtraction(a: int, b: int) -> int:
    """Subtraction function that take two arguments and return the subtraction of them"""
    print("SUBTRACTION FUNCTION IS CALLED")
    return a - b

@tool
def division(a: int, b: int) -> int:
    """Division function that take two arguments and return the division of them"""
    print("DIVISION FUNCTION IS CALLED")
    if b == 0:
        return "Can't divide by zero"
    
    return a / b


# Model

model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.3)

# Agent
tools = [multiplication,addition,subtraction]


prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="""You are a helpful math assistant who explains solutions in Hinglish (Hindi + English mix).
    Follow these rules:
    1. Break down complex expressions using BODMAS rule
    2. Use the available tools (addition, subtraction, multiplication) to solve
    3. Explain each step in simple Hinglish with relatable examples
    4. Always show your calculations
    5. Use proper mathematical terms mixed with Hindi words"""),
    
    # Example 1: Addition
    HumanMessage(content="Solve 5 + 3"),
    AIMessage(content="""Chalo solve karte hain 5 + 3:
    1. Addition tool ka use karenge
    2. 5 aur 3 ko add karenge
    Jaise ki agar aapke paas 5 chocolates hain aur mummy ne 3 aur de diye
    5 + 3 = 8 chocolates ho gayi
    Final answer: 8"""),
    
    # Example 2: Complex Expression
    HumanMessage(content="Solve 10 * 2 + 5"),
    AIMessage(content="""Step by step solve karte hain:
    1. Pehle BODMAS rule ke hisaab se multiplication (10 * 2)
       - Multiplication tool use karenge
       - 10 * 2 = 20
    2. Phir addition karenge (20 + 5)
       - Addition tool use karenge
       - 20 + 5 = 25
    Samjhe beta? Pehle multiplication phir addition kiya
    Final answer: 25"""),
    MessagesPlaceholder(variable_name="aget_scratchpad"), # aget_scratchpad is used to store intermediate values for the agent (like the result of a calculation). If we does not use variable_name = "aget_scratchpad" then it will throw error if we use agent so we have to use variable_name = "aget_scratchpad" in the placeholder otherwise it will throw error
])

# agent = create_openai_tools_agent(llm=model,tools=tools,prompt="")
agent = create_tool_calling_agent(llm=model,tools=tools,prompt=prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    # verbose=True
)

if __name__ == "__main__":
    question = input("Ask your question beta.")

    for chunk in agent_executor.stream({"question":[HumanMessage(content=question)]}):
        if(chunk.get("output")):
            print(chunk["output"])
        time.sleep(0.1)
