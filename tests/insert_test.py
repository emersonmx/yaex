import pytest

from yaex import Context, InvalidOperation, insert


@pytest.fixture
def lines() -> list[str]:
    return ["test\n"]


@pytest.fixture
def context(lines: list[str]) -> Context:
    return Context(1, lines.copy())


def test_should_insert_a_line(context: Context, lines: list[str]) -> None:
    lines.insert(0, "a line\n")
    command = insert("a line")

    result = command(context)

    assert result == Context(1, lines)


def test_should_insert_lines(context: Context, lines: list[str]) -> None:
    lines.insert(0, "a line\n")
    lines.insert(0, "another line\n")

    command = insert("a line")
    context = command(context)
    command = insert("another line")
    result = command(context)

    assert result == Context(1, lines)


def test_should_insert_lines_in_a_single_command(context: Context) -> None:
    expected_lines = ["first line\n", "second line\n", "third line\n", "test\n"]
    command = insert("first line\nsecond line\nthird line\n")

    result = command(context)

    assert result == Context(3, expected_lines)


def test_should_insert_lines_without_trailing_new_line(
    context: Context,
) -> None:
    expected_lines = ["first line\n", "second line\n", "third line\n", "test\n"]
    command = insert("first line\nsecond line\nthird line")

    result = command(context)

    assert result == Context(3, expected_lines)


def test_should_insert_between_lines() -> None:
    context = Context(2, ["first line\n", "third line\n"])
    command = insert("second line")

    result = command(context)

    assert result == Context(
        2,
        ["first line\n", "second line\n", "third line\n"],
    )


def test_should_raise_error_when_insert_into_an_empty_context(
    empty_context: Context,
) -> None:
    command = insert("first line")

    with pytest.raises(InvalidOperation):
        command(empty_context)
