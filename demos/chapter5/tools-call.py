# 0.初始化模型
import os

from dotenv import load_dotenv
from langchain.messages import AIMessage, HumanMessage
from langchain.chat_models import init_chat_model


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

# 本案例验证对象：tools的调用
# 思路：先定义工具，然后验证ai是否能够识别工具列表，最后验证ai是否能调用工具


# 1.定义工具
# 按照之前的学习，利用@tools的装饰器便捷定义工具

from langchain.chat_models import init_chat_model
from langchain.tools import tool


@tool("get_wether",parse_docstring= True)
def get_wether(city : str,is_forecast : bool)-> str : 
    """Get weather information for a city.
        use this tool to get current wether or forecast wether of tommorow

        Args:
            city: Name of the city, such as "Tokyo" or "Osaka".
            is_forecast: Whether to include tomorrow's weather forecast.
                Defaults to False.

        Returns:
            Weather information for the specified city.
    """
    wether = f"今天{city}天气不错/n"
    if(is_forecast):
        wether += ("或多云间晴")
    return wether

# 2.绑定工具，方式：model.bind_tools
# 用简便的语法创建了list，下面message同样

# 这句bind的本质是一个 Runnable[输入, AIMessage] 
# langchain框架告诉ai，我有一个输入是怎么样，输出是怎么样的方法
model_with_tools  = model.bind_tools([get_wether])

# 调试：尝试调用，观察工具链是否加载成功
messages = [HumanMessage("明日观花阜天气如何")]

# 关键是这里会返回什么
# 这里实际上返回的是一个aimessage
# 打开注释可以进入这个类，来自from langchain.messages import AIMessage, HumanMessage
# 里面有个tool_calls，可以看到工具调用请求


response = model_with_tools.invoke(messages)
messages.append(response)
my_tools_calls = response.tool_calls


for tool_call in my_tools_calls:
    # 大模型不能直接调用工具，只能根据你给出的信息来决定你要调用什么工具，所以这里还得自己手动当大模型的助手
    if tool_call["name"] == "get_wether":
        # 这里是langchain通过框架，把大模型返回的消息转换成get_wether的参数，进行了调用
        # 所有的这一切，因为get_wether不是一个普通的方法，它经过@tool装饰之后，是一个别的方法
        # 这里一定是方法名.invoke,千万小心
        
        my_tool_messages =  get_wether.invoke(tool_call)
        messages.append(my_tool_messages)

finalresponse = model.invoke(messages)
messages.append(finalresponse)
for msg in messages:
    msg.pretty_print()
    

    






