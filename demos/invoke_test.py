import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

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

# 字典中，role和content交替使用
messages = [
    {"role": "system", "content": "你是一个文学批评家，你有非常挑剔的文学品味，擅长推荐高水平的书籍"},
    {"role": "user", "content": "给我推荐一本适合入门的小说"},
]
response = model.invoke(messages)
print(response.content)
