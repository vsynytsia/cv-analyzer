import asyncio
import itertools
from collections.abc import Callable, Iterable
from typing import Any


async def execute_tasks_async(
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


def filter_out_exceptions(iterable: Iterable[Any]) -> list[Any]:
    return [item for item in iterable if not isinstance(item, Exception)]


def flatten_2d_list(lst: list[list[Any]]) -> list[Any]:
    return list(itertools.chain.from_iterable(lst))
