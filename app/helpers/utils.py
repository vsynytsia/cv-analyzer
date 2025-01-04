import itertools
from collections.abc import Iterable
from typing import Any


def filter_exceptions(iterable: Iterable[Any]) -> list[Any]:
    return [item for item in iterable if not isinstance(item, Exception)]


def flatten_list(lst: list[list[Any]]) -> list[Any]:
    return list(itertools.chain.from_iterable(lst))
