from collections.abc import Iterable

import pytest

from yaex import Context, InvalidOperation, delete


def make_lines() -> list[str]:
    return [
        "first line\n",
        "second line\n",
        "third line\n",
        "fourth line\n",
        "fifth line\n",
        "sixth line\n",
    ]


def make_ilines() -> Iterable[tuple[int, str]]:
    return enumerate(make_lines(), start=1)


def make_context() -> Context:
    return Context(0, make_lines())


def test_should_delete_a_line() -> None:
    context = make_context()
    expected_lines = make_lines()
    del expected_lines[0]
    command = delete()

    result = command(context)

    assert result == Context(0, expected_lines)


def test_should_delete_lines() -> None:
    context = make_context()
    expected_lines = make_lines()
    del expected_lines[0:2]

    command = delete()
    context = command(context)
    command = delete()
    result = command(context)

    assert result == Context(0, expected_lines)


def test_should_delete_between_lines() -> None:
    context = make_context()
    context.cursor = 1
    expected_lines = make_lines()
    del expected_lines[1]
    command = delete()

    result = command(context)

    assert result == Context(1, expected_lines)


def test_should_raise_error_when_delete_an_empty_context() -> None:
    context = Context(0, [])
    command = delete()

    with pytest.raises(InvalidOperation):
        command(context)


@pytest.mark.parametrize(
    "begin, end, expected_lines",
    [
        (1, 1, [l for i, l in make_ilines() if i != 1]),
        (6, 6, [l for i, l in make_ilines() if i != 6]),
        (2, 2, [l for i, l in make_ilines() if i != 2]),
        (1, 5, [l for i, l in make_ilines() if not (1 <= i <= 5)]),
        (2, 6, [l for i, l in make_ilines() if not (2 <= i <= 6)]),
        (2, 4, [l for i, l in make_ilines() if not (2 <= i <= 4)]),
    ],
)
def test_should_delete_from_range(
    begin: int,
    end: int,
    expected_lines: list[str],
) -> None:
    context = make_context()
    command = delete().from_range(begin, end)

    result = command(context)

    assert result == Context(begin - 1, expected_lines)


@pytest.mark.parametrize(
    "begin, end",
    [
        (0, 0),
        (7, 7),
        (6, 1),
    ],
)
def test_should_raise_error_when_delete_an_invalid_range(
    begin: int,
    end: int,
) -> None:
    context = make_context()
    command = delete().from_range(begin, end)

    with pytest.raises(InvalidOperation):
        command(context)
