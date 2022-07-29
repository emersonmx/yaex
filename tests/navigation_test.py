import pytest

from yaex import Context, InvalidOperation, at_first_line, at_last_line, at_line


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
    command = at_first_line()

    result = command(context)

    assert result.cursor == 0


def test_should_move_cursor_to_last_line() -> None:
    context = make_context()
    command = at_last_line()

    result = command(context)

    assert result.cursor == 5


def test_should_move_cursor_to_any_line() -> None:
    context = make_context()
    command = at_line(3)

    result = command(context)

    assert result.cursor == 2


@pytest.mark.parametrize(
    "line",
    [-100, -1, 0, 7, 100],
)
def test_should_raise_error_when_move_the_cursor_to_an_invalid_line(
    line: int,
) -> None:
    context = make_context()
    command = at_line(line)

    with pytest.raises(InvalidOperation):
        command(context)
