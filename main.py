from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter


load_dotenv()
llm = ChatOpenRouter(
    model="deepseek/deepseek-chat",
    temperature=0
)
response = llm.invoke("简单介绍你是谁")
print(response.content)