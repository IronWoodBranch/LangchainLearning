## day1笔记

langchain家族的用法：

Langchain-core 
Langchain-classic
被丢弃的

langgraph：底层

Classic

langchain：基础
langgraph：编排复杂的智能体
Deep agent：基础的agent的编排

RAG
检索增强生成
Retrieval augmented generation

RAG难点；
1.文件解析，各种不同的文件
2.文件切割：对不同的文件的处理
    切成不同的chunks
    最常用：递归字符
3.向量数据库的检索
4.reranker的抉择（重排序，成本高，简单问题不做，也许是快速模式的反馈）
5.
规划能力，记忆能力，工具，行动能力

短期记忆，长期记忆（横跨周期）

python里面os.getEnv来拿api key
我在想，c#的项目通常通过常量/依赖注入直接注入配置文件，感觉做法不太一样

temprature越高，创造力越强，但相应的幻觉可能越严重

Init_chat_model

其中的max_token参数可以由大模型自己直接截断，可以真正的省钱

ollama可以做本地大模型

## day2笔记

- loadEnv函数带参数true
  - 是因为这个参数有时候能从环境变量里面du，带了参数true确保从自己的配置文件里面读，最高优先
- model = init_chat_model(
model="google/gemini-2.5-flash-lite",
model_provider="openai",
api_key=Api_key_openrouter,
base_url="[https://openrouter.ai/api/v1](https://openrouter.ai/api/v1)",
)
这种写法，由于是可变参数，所以按顺序调的话，仍然不能省略参数名，不能按顺序传，否则报错；
  - 只有第一个参数能不指定参数名
- 角色
  1. 这里的角色不是那种跟ai聊天的时候随便定义什么角色都可以的，而是langchain和各个模型商规定了几种角色，如果随意输入自己的角色，可能会导致报错
  2. system:System,eg."你是一个专业的python老师"
  3. user:Human/User,这里其实要装问题,eg:"xxxx这句代码为什么报错，我犯了什么语法错误"
    - 建议一致用user而非human，各提供商中惯用“user”
  4. assistant:AI/Assistant,AI的历史回复（上下文等等）

- 涉及多轮对话，那就要把之前的回复也加入assistant里面去

- 优化：现成的用法：
  - 有SystemMessasge()，HumanMessage方法能把消息直接封装起来，指定role，content可以简单化

