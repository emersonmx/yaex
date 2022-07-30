import pytest

from yaex import Context, InvalidOperation, search


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


def test_should_move_cursor_to_found_line() -> None:
    context = make_context()
    expected_lines = context.lines.copy()
    command = search("fourth line")

    result = command(context)

    assert result == Context(3, expected_lines)


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


def test_should_search_lines_in_loop() -> None:
    context = make_context()
    expected_lines = context.lines.copy()
    command = search("first")

    result = command(context)

    assert result == Context(0, expected_lines)


def test_should_start_reverse_search_from_current_line() -> None:
    context = Context(
        2,
        [
            "first line\n",
            "\n",
            "third line\n",
            "fourth line\n",
            "\n",
            "sixth line\n",
        ],
    )
    expected_lines = context.lines.copy()
    command = search(r"^$", reverse=True)

    result = command(context)

    assert result == Context(1, expected_lines)


def test_should_raise_error_when_not_found_the_pattern() -> None:
    context = Context(0, [])
    command = search("unknown line")

    with pytest.raises(InvalidOperation):
        command(context)
