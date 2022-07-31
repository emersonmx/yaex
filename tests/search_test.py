import pytest

from yaex import Context, InvalidOperation, search


def make_context() -> Context:
    return Context(
        2,
        [
            "first line\n",
            "\n",
            "third line\n",
            "\n",
            "fifth line\n",
        ],
    )


def test_should_move_cursor_to_found_line() -> None:
    context = make_context()
    expected_lines = context.lines.copy()
    command = search("fifth line")

    result = command(context)

    assert result == Context(4, expected_lines)


def test_should_move_cursor_to_found_line_with_regex() -> None:
    context = make_context()
    expected_lines = context.lines.copy()
    command = search(r"^fifth .*")

    result = command(context)

    assert result == Context(4, expected_lines)


def test_should_start_search_from_current_line() -> None:
    context = make_context()
    expected_lines = context.lines.copy()
    command = search("line")

    result = command(context)

    assert result == Context(2, expected_lines)


def test_should_make_a_loop_search_until_current_line() -> None:
    context = make_context()
    expected_lines = context.lines.copy()
    command = search("first")

    result = command(context)

    assert result == Context(0, expected_lines)


def test_should_move_cursor_to_found_line_in_reverse() -> None:
    context = make_context()
    expected_lines = context.lines.copy()
    command = search("first").in_reverse()

    result = command(context)

    assert result == Context(0, expected_lines)


def test_should_start_reverse_search_from_previous_line() -> None:
    context = make_context()
    expected_lines = context.lines.copy()
    command = search("line").in_reverse()

    result = command(context)

    assert result == Context(0, expected_lines)


def test_should_make_a_reverse_loop_search_until_current_line() -> None:
    context = make_context()
    expected_lines = context.lines.copy()
    command = search(r"^$").in_reverse()

    result = command(context)

    assert result == Context(1, expected_lines)


def test_should_raise_error_when_pattern_not_found() -> None:
    context = Context(0, [])
    command = search("unknown line")

    with pytest.raises(InvalidOperation):
        command(context)
