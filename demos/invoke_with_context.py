import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

# override=True: 若系统环境里已有同名变量，用 .env 里的值覆盖它
load_dotenv(override=True)
Api_key_openrouter = os.getenv("OPENROUTER_API_KEY")
# 通过 OpenAI 兼容接口调用 OpenRouter
model = init_chat_model(
    model="google/gemini-2.5-flash-lite",
    model_provider="openai",
    # - api_key / base_url: 指向 OpenRouter，而不是官方 OpenAI
    api_key=Api_key_openrouter,
    base_url="https://openrouter.ai/api/v1",
)

# 原本版本
message1 = [
    {"role": "system", "content": "你是一个小说家，名字叫A"},
    {"role": "user", "content": "你好我叫小王"},
]

# 优化版本
message_simple = [
    SystemMessage(content="你是一个小说家，名字叫A"),
    HumanMessage(content="你好我叫小王"),
]


response1 = model.invoke(message1)
print(response1.content)

# 这就是没有记忆的版本
# message2 =[
#     {"role":"user","content":"我叫什么，你叫什么"}
# ]

#有记忆的版本
message1.append({"role":"assistant","content":response1.content})
response2 = model.invoke(message1)
print(response2.content)

