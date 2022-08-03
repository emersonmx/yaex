import pytest

from yaex import Context, InvalidOperation, substitute


def make_context() -> Context:
    return Context(
        0,
        [
            "first line first line first line\n",
            "second line second line second line\n",
            "third line third line third line\n",
        ],
    )


def test_should_substitute_a_text_one_time() -> None:
    context = make_context()
    expected_lines = context.lines.copy()
    expected_lines[0] = "first LINE first line first line\n"
    command = substitute("line", "LINE")

    result = command(context)

    assert result == Context(0, expected_lines)


def test_should_substitute_a_text_many_times() -> None:
    context = make_context()
    expected_lines = context.lines.copy()
    expected_lines[0] = "1st line 1st line first line\n"
    command = substitute("first", "1st").times(2)

    result = command(context)

    assert result == Context(0, expected_lines)


def test_should_substitute_a_text_every_time() -> None:
    context = make_context()
    expected_lines = context.lines.copy()
    expected_lines[0] = "1st line 1st line 1st line\n"
    command = substitute("first", "1st").every_time()

    result = command(context)

    assert result == Context(0, expected_lines)


def test_should_raise_error_when_text_not_found() -> None:
    context = make_context()
    command = substitute("fourth", "4th")

    with pytest.raises(InvalidOperation):
        command(context)
