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


- gather
  - 约等于task.whenall
  - Tips，记得不能传List<Task>(C#的思维的说法)，要拆开，拆箱的便捷工具: *


- 协程任务和C#的巨大差异
        batch_task = asyncio.create_task(batch_coroutines_execute())
        print("协程已启动") 
        await asyncio.sleep(0.5)
        results = await batch_task
    流程解释：
    1.create_task这里创建协程任务，但是不启动，跟c#有点神似的地方是Create_Task的参数是个委托，这里把几个方法传进去了，等待执行（但实际不是这样，暂且按这样记忆）
    2.asyncio.sleep的方法，让main暂停0.5秒并且让出控制权，同时协程开始启动并且等待
    3.results = await batch_task这里只是等待一个结果，并非启动，这里是最容易误解的
    
  - 主程和协程的转化：
    - 如果有await的操作，大部分情况主程会闲下来，闲得无聊就会开启协程任务
    - 但有一个情况例外：例如前面由create_task安排的任务非常早之前就完成了，这个时候result = await 安排的任务，一秒都不会闲下来，所以这个时候不会让时间给协程
  

- f类似于C#的$

- 收获清单
  1. Python 调用异步函数不等于启动执行。
  2. create_task 和 await task 职责不同。
  3. await 暂停的是当前协程，不是整个程序


- chatopenRouter等方法的返回值里面有一个proflie属性，能看到一些基本信息，例如temprature等等
  - 例如：同一个chatopenrouter，里面的模型换了，gpt5.5,flash 3.0之类的，返回值里就能看到model.profile是否是不同的

- Init_chat_model创建的model的额外字段
  - langchain没有直接列出来的字段，但是模型支持的话，我们可以手动给它加到Model kwargs里面去
  Eg.可选参数，可以指定调用什么tools

  - extra_body
    - 个性化的字段，不同厂商的独特字段，在Init_chat_model里面总要留出这种灵活字段
  
  - configurable：
    - 和init_chatmodel的参数都一样，但如果设置了这个参数，会覆盖init_chat_model中的设置，也就是某些单词要进行特殊设置的时候，可以选用这个参数


# day 4
- 输入格式化content_blocks
  - 多模态的使用等等情况会不一样：具体做法查看文档
  - 按照规范，content里面需要放字典list来表达多模态
    但是不同供应商的标准不一样，所以需要用到content_blocks

- 输出模式格式化：也是它content_blocks


- 提示词模板 promts templates
  - 可以防注入，标准化，很多有点，正式开发最好启用
  - chatPromtpTemplate.from_messages()/chatPromtpTemplate()都可以/还有个formatt（）方法
  - from_messages有多种调用方法，但我感觉不改变其本质，能用就行


- 原始模板可以抠出关键的身份，信息，把场景提供出来，然后不同的输入可以快速复用同一个模板
  - 可以用partial来简化代码

- 消息占位符：多轮对话中可以使用这个技巧
  - 可以在多轮对话中，动态嵌入用户的历史回复和技巧


- 工具的使用：
  - 以前：function calling
  - 现在: MCP
  1. 调用方式：
    1. 直接调用:xxx.xxxx 用.来直接调用
    2. 基于模型进行调用:
      1. 用bind_tools[]来绑定工具
      2. 我的理解：可以内置，自己提供工具绑定列表，让别的模型为自己决定调用哪个工具
- 工具的定义：
    - 参数用comment进行说明，用自然语言，遵循一定规范（谷歌规范优先）
    - 最好用@tool装饰器，有内置的方法，能省很多功夫
    - 可以直接把这个工具的作用加到tool(description里面，但我的直觉告诉我，这肯定不符合最佳规范，就把所有接口参数都解释清楚更好，记得添加Parse_doc的参数，能将这个说明给格式化)
    - 有一些别的参数，可以规定多个名字之类，我判断：无意义
  
- pydatic
  - 可以辅助规定输入输出的格式等等

