from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field


load_dotenv()

class ResponseFormatter(BaseModel):
    """Always use this tool to structure your response to the user."""
    name: str = Field(description="A name which is there on the user's question")
    bike: str = Field(description="A bike name which is there on the user's question")


llm = ChatOpenAI(model_name="gpt-4o-mini")


prompt = ChatPromptTemplate(
    [
        ('system','you are math assistant. can you give the answer in hinglish only does not use pure english if you say in english you have to give answer in hinglish only and answer should be in short'),
        MessagesPlaceholder(variable_name="ques")
    ]
)


if __name__ == "__main__":
    question = input("Ask you questions:- ")
    message = prompt.format_messages(ques = [HumanMessage(content=question)])

    model_with_tool = llm.bind_tools([ResponseFormatter])

    # for chunk in llm.stream(message):
    #     print(chunk.content,end="",flush=True)

    print(model_with_tool.invoke(message))