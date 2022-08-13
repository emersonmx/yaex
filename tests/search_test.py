import pytest

from yaex import Context, InvalidOperation, search


@pytest.fixture
def lines() -> list[str]:
    return [
        "first line\n",
        "\n",
        "third line\n",
        "\n",
        "fifth line\n",
    ]


@pytest.fixture
def context(lines: list[str]) -> Context:
    return Context(2, lines.copy())


def test_should_move_cursor_to_found_line(
    context: Context,
    lines: list[str],
) -> None:
    command = search("fifth line")

    result = command(context)

    assert result == Context(4, lines)


def test_should_move_cursor_to_found_line_with_regex(
    context: Context,
    lines: list[str],
) -> None:
    command = search(r"^fifth .*")

    result = command(context)

    assert result == Context(4, lines)


def test_should_start_search_from_current_line(
    context: Context,
    lines: list[str],
) -> None:
    command = search("line")

    result = command(context)

    assert result == Context(2, lines)


def test_should_make_a_loop_search_until_current_line(
    context: Context,
    lines: list[str],
) -> None:
    command = search("first")

    result = command(context)

    assert result == Context(0, lines)


def test_should_move_cursor_to_found_line_in_reverse(
    context: Context,
    lines: list[str],
) -> None:
    command = search("first").in_reverse()

    result = command(context)

    assert result == Context(0, lines)


def test_should_start_reverse_search_from_previous_line(
    context: Context,
    lines: list[str],
) -> None:
    command = search("line").in_reverse()

    result = command(context)

    assert result == Context(0, lines)


def test_should_make_a_reverse_loop_search_until_current_line(
    context: Context,
    lines: list[str],
) -> None:
    command = search(r"^$").in_reverse()

    result = command(context)

    assert result == Context(1, lines)


def test_should_raise_error_when_pattern_not_found(
    empty_context: Context,
) -> None:
    command = search("unknown line")

    with pytest.raises(InvalidOperation):
        command(empty_context)
