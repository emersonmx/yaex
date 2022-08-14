import pytest

from yaex.commands import (
    Context,
    InvalidOperation,
    LineNumber,
    raise_for_line_number,
    split_lines_at_cursor,
    to_index,
    to_line,
)


@pytest.mark.parametrize("line", [-10, -7, 0, 7, 10])
def test_should_raise_error_when_in_invalid_range(
    line: LineNumber,
    context: Context,
) -> None:
    with pytest.raises(InvalidOperation):
        raise_for_line_number(line, context)


def test_should_split_lines_at_cursor(
    lines: list[str],
) -> None:
    splits = split_lines_at_cursor(lines, 3)
    expected_splits = lines[:2], lines[2:]
    assert splits == expected_splits


def test_should_convert_a_line_index_to_line_number() -> None:
    assert to_line(-1) == 0
    assert to_line(0) == 1
    assert to_line(1) == 2


def test_should_convert_a_line_number_to_line_index() -> None:
    assert to_index(0) == -1
    assert to_index(1) == 0
    assert to_index(2) == 1
