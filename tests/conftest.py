from collections.abc import Iterable

import pytest

from yaex.commands import Context


@pytest.fixture
def lines() -> list[str]:
    return [
        "first line\n",
        "second line\n",
        "third line\n",
        "fourth line\n",
        "fifth line\n",
        "sixth line\n",
    ]


@pytest.fixture
def ilines(lines: list[str]) -> Iterable[tuple[int, str]]:
    return enumerate(lines.copy(), start=1)


@pytest.fixture
def empty_context() -> Context:
    return Context(1, [])


@pytest.fixture
def context(lines: list[str]) -> Context:
    lines_copy = lines.copy()
    return Context(1, lines_copy)
