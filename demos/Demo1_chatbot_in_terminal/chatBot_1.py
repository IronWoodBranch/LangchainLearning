import os

from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter


def keep_recent_messages(
    messages: list[dict[str, str]],
    max_pairs: int = 3
) -> list[dict[str, str]]:
    # 保留 system 消息
    system_messages = [
        message
        for message in messages
        if message.get("role") == "system"
    ]

    # 获取 user 和 assistant 消息
    conversation_messages = [
        message
        for message in messages
        if message.get("role") != "system"
    ]

    # 暂时只保留最近若干条消息
    recent_messages = conversation_messages[-(max_pairs * 2):]

    return system_messages + recent_messages


load_dotenv()

if not os.getenv("OPENROUTER_API_KEY"):
    raise RuntimeError("没有读取到 OPENROUTER_API_KEY，请检查 .env 文件")


model = ChatOpenRouter(
    model="google/gemini-2.5-flash-lite"
)


messages = [
    {
        "role": "system",
        "content": (
            "你是一个小学教师，你很擅长把复杂抽象的问题具象化，"
            "找到即便小孩也能理解的解释方式。"
        )
    }
]


round_index = 1

while True:
    print(f"\n这是第 {round_index} 轮对话，输入 Q 退出")

    user_input = input("我：").strip()

    if user_input.upper() == "Q":
        break

    # 先把当前用户问题加入历史
    messages.append({
        "role": "user",
        "content": user_input
    })

    memory_messages = keep_recent_messages(messages)

    print("老师：", end="", flush=True)

    reply_content = ""

    for chunk in model.stream(memory_messages):
        if chunk.content:
            print(chunk.content, end="", flush=True)
            reply_content += chunk.content

    # 把完整的助手回复加入历史
    messages.append({
        "role": "assistant",
        "content": reply_content
    })

    print(f"\n第 {round_index} 轮对话结束")

    round_index += 1