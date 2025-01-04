import asyncio
import itertools
import logging
from collections.abc import Iterable
from typing import Any, Callable, Sequence, TypeVar

import jinja2

__all__ = ["filter_exceptions", "flatten_list", "chunk", "gather", "get_rendered_template"]

logger = logging.getLogger(__name__)

T = TypeVar("T")


def filter_exceptions(iterable: Iterable[Any]) -> list[Any]:
    iterable_without_exceptions = []
    for item in iterable:
        if isinstance(item, Exception):
            logger.warning("Encountered exception while filtering: %s", str(item))
        else:
            iterable_without_exceptions.append(item)
    return iterable_without_exceptions


def flatten_list(lst: list[list[Any]]) -> list[Any]:
    return list(itertools.chain.from_iterable(lst))


def chunk(s: Sequence[T], chunk_size: int = 5) -> list[Sequence[T]]:
    return [s[i : i + chunk_size] for i in range(0, len(s), chunk_size)]


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


def get_rendered_template(env: jinja2.Environment, template_path: str, **kwargs) -> str:
    template = env.get_template(template_path)
    return template.render(**kwargs)
