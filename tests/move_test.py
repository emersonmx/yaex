import pytest

from yaex import Context, InvalidOperation, move


def make_context() -> Context:
    return Context(
        2,
        [
            "first line\n",
            "second line\n",
            "third line\n",
            "fourth line\n",
            "fifth line\n",
        ],
    )


def test_should_stay_at_same_line() -> None:
    context = make_context()
    expected_lines = context.lines.copy()
    command = move(0)

    result = command(context)

    assert result == Context(2, expected_lines)


def test_should_move_to_next_line() -> None:
    context = make_context()
    expected_lines = context.lines.copy()
    command = move(1)

    result = command(context)

    assert result == Context(3, expected_lines)


def test_should_move_to_previous_line() -> None:
    context = make_context()
    expected_lines = context.lines.copy()
    command = move(-1)

    result = command(context)

    assert result == Context(1, expected_lines)


@pytest.mark.parametrize(
    "offset",
    [-10, -3, 3, 10],
)
def test_should_raise_error_when_invalid_move(offset: int) -> None:
    context = make_context()
    command = move(offset)

    with pytest.raises(InvalidOperation):
        command(context)
