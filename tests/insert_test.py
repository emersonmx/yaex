import pytest

from yaex import Context, InvalidOperation, insert


def make_context() -> Context:
    return Context(0, ["test\n"])


def test_should_insert_a_line() -> None:
    context = make_context()
    command = insert("a line")

    result = command(context)

    assert result == Context(0, ["a line\n", "test\n"])


def test_should_insert_lines() -> None:
    context = make_context()

    command = insert("a line")
    context = command(context)
    command = insert("another line")
    result = command(context)

    assert result == Context(0, ["another line\n", "a line\n", "test\n"])


def test_should_insert_lines_in_a_single_command() -> None:
    context = make_context()
    command = insert("first line\nsecond line\nthird line\n")

    result = command(context)

    assert result == Context(
        2,
        ["first line\n", "second line\n", "third line\n", "test\n"],
    )


def test_should_insert_lines_without_trailing_new_line() -> None:
    context = make_context()
    command = insert("first line\nsecond line\nthird line")

    result = command(context)

    assert result == Context(
        2,
        ["first line\n", "second line\n", "third line\n", "test\n"],
    )


def test_should_insert_between_lines() -> None:
    context = Context(1, ["first line\n", "third line\n"])
    command = insert("second line")

    result = command(context)

    assert result == Context(
        1,
        ["first line\n", "second line\n", "third line\n"],
    )


def test_should_raise_error_when_insert_into_an_empty_context() -> None:
    context = Context(0, [])
    command = insert("first line")

    with pytest.raises(InvalidOperation):
        command(context)
