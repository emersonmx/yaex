import pytest

from yaex import Context, InvalidOperation, delete


def make_context() -> Context:
    return Context(0, ["first line\n", "second line\n", "third line\n"])


def test_should_delete_a_line() -> None:
    context = make_context()
    command = delete()

    result = command(context)

    assert result == Context(0, ["second line\n", "third line\n"])


def test_should_delete_lines() -> None:
    context = make_context()

    command = delete()
    context = command(context)
    command = delete()
    result = command(context)

    assert result == Context(0, ["third line\n"])


def test_should_delete_between_lines() -> None:
    context = Context(1, ["first line\n", "second line\n", "third line\n"])
    command = delete()

    result = command(context)

    assert result == Context(1, ["first line\n", "third line\n"])


def test_should_raise_error_when_delete_an_empty_context() -> None:
    context = Context(0, [])
    command = delete()

    with pytest.raises(InvalidOperation):
        command(context)
