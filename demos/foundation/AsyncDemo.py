import asyncio
import time


async def fake_model(index:int) -> str:
    print(f"任务{index}开始")
    # 睡两秒
    await asyncio.sleep(2)
    print(f"任务{index}结束")
    return f"结果{index}"


async def batch_coroutines_execute() -> list[str]:
    # py里面创建协程但是不执行
    coroutines = [
        fake_model(1),
        fake_model(2),
        fake_model(3)
    ]

    #想要执行得手动执行
    #  这里*的语法是把List<协程>拆开拆成三个单独的协程，以供gather调用
    response = await asyncio.gather(*coroutines)
    return response


async def main() -> None:
    start_time = time.perf_counter()
    # 这里以异步的方式启动任务
    batch_task = asyncio.create_task(batch_coroutines_execute())
    print("协程已启动")
    await asyncio.sleep(0.5)
    results = await batch_task
    print(results)
    print(f"总耗时：{time.perf_counter() - start_time:.2f} 秒")


if __name__ == "__main__":
    asyncio.run(main())