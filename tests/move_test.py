import pytest

from yaex import Context, InvalidOperation, move


@pytest.fixture
def context(context: Context) -> Context:
    context.cursor = 2
    return context


def test_should_stay_at_same_line(context: Context, lines: list[str]) -> None:
    command = move(0)

    result = command(context)

    assert result == Context(2, lines)


def test_should_move_to_next_line(context: Context, lines: list[str]) -> None:
    command = move(1)

    result = command(context)

    assert result == Context(3, lines)


def test_should_move_to_previous_line(
    context: Context,
    lines: list[str],
) -> None:
    command = move(-1)

    result = command(context)

    assert result == Context(1, lines)


@pytest.mark.parametrize(
    "offset",
    [-10, -5, -2, 5, 10],
)
def test_should_raise_error_when_invalid_move(
    offset: int,
    context: Context,
) -> None:
    command = move(offset)

    with pytest.raises(InvalidOperation):
        command(context)
