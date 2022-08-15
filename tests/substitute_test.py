import re

import pytest

from yaex import (
    Context,
    InvalidOperation,
    go_to,
    go_to_first_line,
    go_to_last_line,
    move,
    search,
    substitute,
)
from yaex.commands import LineNumber, LineResolver, make_line_resolver_callbacks


@pytest.fixture
def lines() -> list[str]:
    return [
        "first line first line first line\n",
        "second line second line second line\n",
        "third line third line third line\n",
        "fourth line fourth line fourth line\n",
        "fifth line fifth line fifth line\n",
        "sixth line sixth line sixth line\n",
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


@pytest.mark.parametrize(
    "begin, end, search_regex, replace_regex, count, cursor",
    [
        (2, 2, "line", "LINE", 1, 2),
        (1, 1, "line", "LINE", 1, 1),
        (6, 6, "line", "LINE", 1, 6),
        (1, 6, "line", "LINE", 1, 6),
        (1, 5, "line", "LINE", 1, 5),
        (2, 6, "line", "LINE", 1, 6),
        (2, 5, "line", "LINE", 1, 5),
        (2, 5, "second", "2nd", 1, 2),
        (2, 5, "third", "3rd", 1, 3),
        (2, 5, "fifth", "5th", 1, 5),
        (2, go_to(5), "third", "3rd", 1, 3),
        (go_to(2), 5, "third", "3rd", 1, 3),
        (go_to(2), go_to(5), "third", "3rd", 1, 3),
        (2, move(4), "third", "3rd", 1, 3),
        (move(1), 5, "third", "3rd", 1, 3),
        (move(1), move(4), "third", "3rd", 1, 3),
        (1, go_to_last_line(), "line", "LINE", 1, 6),
        (go_to_first_line(), 6, "line", "LINE", 1, 6),
        (go_to_first_line(), go_to_last_line(), "line", "LINE", 1, 6),
        (2, search("fifth"), "third", "3rd", 1, 3),
        (search("second"), 5, "third", "3rd", 1, 3),
        (search("second"), search("fifth"), "third", "3rd", 1, 3),
    ],
)
def test_should_substitute_a_text_from_range(
    begin: LineResolver,
    end: LineResolver,
    search_regex: str,
    replace_regex: str,
    count: int,
    cursor: LineNumber,
    context: Context,
) -> None:
    begin_resolver, end_resolver = make_line_resolver_callbacks(begin, end)
    lines = []
    for line_number, line_text in enumerate(context.lines.copy(), start=1):
        new_line = line_text
        begin_line = begin_resolver._resolve_line(context)
        end_line = end_resolver._resolve_line(context)
        if begin_line <= line_number <= end_line:
            new_line = re.sub(search_regex, replace_regex, line_text, count)
        lines.append(new_line)

    command = substitute(search_regex, replace_regex).from_range(begin, end)

    result = command(context)

    assert result == Context(cursor, lines)


def test_should_raise_error_when_text_not_found(context: Context) -> None:
    command = substitute("fourth", "4th")

    with pytest.raises(InvalidOperation):
        command(context)
