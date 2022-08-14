from collections.abc import Callable, Iterable

import pytest

from yaex import (
    Context,
    InvalidOperation,
    delete,
    go_to,
    go_to_first_line,
    go_to_last_line,
    move,
    search,
)
from yaex.commands import LineResolver


def test_should_delete_a_line(context: Context, lines: list[str]) -> None:
    del lines[0]
    command = delete()

    result = command(context)

    assert result == Context(1, lines)


def test_should_delete_lines(context: Context, lines: list[str]) -> None:
    del lines[0:2]

    command = delete()
    context = command(context)
    command = delete()
    result = command(context)

    assert result == Context(1, lines)


def test_should_delete_between_lines(
    context: Context,
    lines: list[str],
) -> None:
    context.cursor = 2
    del lines[1]
    command = delete()

    result = command(context)

    assert result == Context(2, lines)


def test_should_raise_error_when_delete_an_empty_context(
    empty_context: Context,
) -> None:
    command = delete()

    with pytest.raises(InvalidOperation):
        command(empty_context)


@pytest.mark.parametrize(
    "begin, end, line_filter",
    [
        (1, 1, lambda i: i != 1),
        (6, 6, lambda i: i != 6),
        (2, 2, lambda i: i != 2),
        (1, 5, lambda i: not (1 <= i <= 5)),
        (2, 6, lambda i: not (2 <= i <= 6)),
        (2, 4, lambda i: not (2 <= i <= 4)),
        (go_to_first_line(), 5, lambda i: i == 6),
        (2, go_to_last_line(), lambda i: i == 1),
        (go_to_first_line(), go_to_last_line(), lambda _: False),
        (2, go_to(5), lambda i: not (2 <= i <= 5)),
        (go_to(2), 5, lambda i: not (2 <= i <= 5)),
        (go_to(2), go_to(5), lambda i: not (2 <= i <= 5)),
        (2, move(4), lambda i: not (2 <= i <= 5)),
        (move(1), 5, lambda i: not (2 <= i <= 5)),
        (move(1), move(4), lambda i: not (2 <= i <= 5)),
        (2, search("fifth"), lambda i: not (2 <= i <= 5)),
        (search("second"), 5, lambda i: not (2 <= i <= 5)),
        (search("second"), search("fifth"), lambda i: not (2 <= i <= 5)),
    ],
)
def test_should_delete_from_range(
    begin: LineResolver,
    end: LineResolver,
    line_filter: Callable[[int], bool],
    context: Context,
    ilines: Iterable[tuple[int, str]],
) -> None:
    expected_lines = [l for i, l in ilines if line_filter(i)]
    command = delete().from_range(begin, end)
    if not isinstance(begin, int):
        begin = begin._resolve_line(context)

    result = command(context)

    assert result == Context(begin, expected_lines)


@pytest.mark.parametrize(
    "begin, end",
    [
        (0, 0),
        (7, 7),
        (6, 1),
        (6, go_to_first_line()),
        (go_to_last_line(), 1),
        (go_to_last_line(), go_to_first_line()),
        (0, go_to(0)),
        (go_to(0), 0),
        (go_to(0), go_to(0)),
        (7, go_to(7)),
        (go_to(7), 7),
        (go_to(7), go_to(7)),
        (6, go_to(1)),
        (go_to(6), 1),
        (go_to(6), go_to(1)),
        (0, move(-1)),
        (move(-1), 0),
        (move(-1), move(-1)),
        (7, move(7)),
        (move(7), 7),
        (move(7), move(7)),
        (6, move(1)),
        (move(5), 0),
        (move(5), move(1)),
    ],
)
def test_should_raise_error_when_delete_an_invalid_range(
    context: Context,
    begin: LineResolver,
    end: LineResolver,
) -> None:
    command = delete().from_range(begin, end)

    with pytest.raises(InvalidOperation):
        command(context)
