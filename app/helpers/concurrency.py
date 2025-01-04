import asyncio
from typing import Any, Callable, Iterable


async def gather(
    items: Iterable[Any],
    coro_factory: Callable,
    post_processor: Callable[[list[Any]], Any] = lambda x: x,
    return_exceptions: bool = True,
) -> Any:
    tasks = []
    for item in items:
        coro = coro_factory(item)
        tasks.append(asyncio.create_task(coro))

    results = await asyncio.gather(*tasks, return_exceptions=return_exceptions)
    return post_processor(results)
