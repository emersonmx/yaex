import pytest

from yaex import Context, InvalidOperation, substitute


@pytest.fixture
def lines() -> list[str]:
    return [
        "first line first line first line\n",
        "second line second line second line\n",
        "third line third line third line\n",
    ]


@pytest.fixture
def context(lines: list[str]) -> Context:
    return Context(1, lines.copy())


def test_should_substitute_a_text_one_time(
    context: Context,
    lines: list[str],
) -> None:
    lines[0] = "first LINE first line first line\n"
    command = substitute("line", "LINE")

    result = command(context)

    assert result == Context(1, lines)


def test_should_substitute_a_text_many_times(
    context: Context,
    lines: list[str],
) -> None:
    lines[0] = "1st line 1st line first line\n"
    command = substitute("first", "1st").times(2)

    result = command(context)

    assert result == Context(1, lines)


def test_should_substitute_a_text_every_time(
    context: Context,
    lines: list[str],
) -> None:
    lines[0] = "1st line 1st line 1st line\n"
    command = substitute("first", "1st").every_time()

    result = command(context)

    assert result == Context(1, lines)


def test_should_raise_error_when_text_not_found(context: Context) -> None:
    command = substitute("fourth", "4th")

    with pytest.raises(InvalidOperation):
        command(context)
