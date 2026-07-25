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

6.
短期记忆，长期记忆（横跨周期）

python里面os.getEnv来拿api key
我在想，c#的项目通常通过常量/依赖注入直接注入配置文件，感觉做法不太一样
 

temprature越高，创造力越强，但相应的幻觉可能越严重


Init_chat_model

其中的max_token参数可以由大模型自己直接截断，可以真正的省钱

ollama可以做本地大模型