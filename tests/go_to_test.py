import pytest

from yaex import (
    Context,
    InvalidOperation,
    go_to,
    go_to_first_line,
    go_to_last_line,
)


def test_should_move_cursor_to_first_line(
    context: Context,
    lines: list[str],
) -> None:
    command = go_to_first_line()

    result = command(context)

    assert result == Context(1, lines)


def test_should_move_cursor_to_last_line(
    context: Context,
    lines: list[str],
) -> None:
    command = go_to_last_line()

    result = command(context)

    assert result == Context(len(lines), lines)


def test_should_move_cursor_to_any_line(
    context: Context,
    lines: list[str],
) -> None:
    command = go_to(3)

    result = command(context)

    assert result == Context(3, lines)


@pytest.mark.parametrize(
    "line",
    [-100, -1, 0, 7, 100],
)
def test_should_raise_error_when_move_the_cursor_to_an_invalid_line(
    line: int,
    context: Context,
) -> None:
    command = go_to(line)

    with pytest.raises(InvalidOperation):
        command(context)
