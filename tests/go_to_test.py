import pytest

from yaex import (
    Context,
    InvalidOperation,
    go_to,
    go_to_first_line,
    go_to_last_line,
)


def make_context() -> Context:
    return Context(
        0,
        [
            "first line\n",
            "second line\n",
            "third line\n",
            "fourth line\n",
            "fifth line\n",
            "sixth line\n",
        ],
    )


def test_should_move_cursor_to_first_line() -> None:
    context = make_context()
    expected_lines = context.lines.copy()
    command = go_to_first_line()

    result = command(context)

    assert result == Context(0, expected_lines)


def test_should_move_cursor_to_last_line() -> None:
    context = make_context()
    expected_lines = context.lines.copy()
    command = go_to_last_line()

    result = command(context)

    assert result == Context(5, expected_lines)


def test_should_move_cursor_to_any_line() -> None:
    context = make_context()
    expected_lines = context.lines.copy()
    command = go_to(3)

    result = command(context)

    assert result == Context(2, expected_lines)


@pytest.mark.parametrize(
    "line",
    [-100, -1, 0, 7, 100],
)
def test_should_raise_error_when_move_the_cursor_to_an_invalid_line(
    line: int,
) -> None:
    context = make_context()
    command = go_to(line)

    with pytest.raises(InvalidOperation):
        command(context)
