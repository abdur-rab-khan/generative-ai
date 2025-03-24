from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable,RunnableLambda

load_dotenv()

llm_model = ChatOpenAI(model="gpt-4o-mini",temperature=0.3)

# runnable = RunnableLambda(lambda x:str(x))

# value = runnable.invoke(5) ---> It is only used of single input

# value = runnable.batch([4,5,6,7]) ---> It is used for transform the out of multiple values

def func(y):
    for x in y:
        yield x

runnable = RunnableLambda(func)

for chunk in runnable.stream(range(5)):
    print(chunk) 