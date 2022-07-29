import pytest

from yaex import Context, InvalidOperation, delete


def make_context() -> Context:
    return Context(0, ["first line\n", "second line\n", "third line\n"])


def test_should_delete_a_line() -> None:
    context = make_context()

    command = delete()
    result = command(context)

    assert result.cursor == 0
    assert result.lines == ["second line\n", "third line\n"]
    assert len(result.lines) == 2


def test_should_delete_lines() -> None:
    context = make_context()

    command = delete()
    context = command(context)
    command = delete()
    result = command(context)

    assert result.cursor == 0
    assert result.lines == ["third line\n"]
    assert len(result.lines) == 1


def test_should_delete_between_lines() -> None:
    context = Context(1, ["first line\n", "second line\n", "third line\n"])

    command = delete()
    result = command(context)

    assert result.cursor == 1
    assert result.lines == [
        "first line\n",
        "third line\n",
    ]
    assert len(result.lines) == 2


def test_should_raise_error_when_delete_an_empty_context() -> None:
    context = Context(0, [])
    command = delete()

    with pytest.raises(InvalidOperation):
        command(context)
