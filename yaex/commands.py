import re
from collections.abc import Iterable
from dataclasses import dataclass
from itertools import cycle, islice
from typing import Protocol


class InvalidOperation(Exception):
    pass


LineNumber = int
LineIndex = int
LineOffset = int


@dataclass
class Context:
    cursor: LineNumber
    lines: list[str]


class Command(Protocol):
    def __call__(self, context: Context) -> Context:
        ...


class GoToFirstLineCommand:
    def __call__(self, context: Context) -> Context:
        context.cursor = 1
        return context


class GoToLastLineCommand:
    def __call__(self, context: Context) -> Context:
        context.cursor = len(context.lines)
        return context


class GoToCommand:
    def __init__(self, line: LineNumber) -> None:
        self.line = line

    def __call__(self, context: Context) -> Context:
        raise_for_line_number(self.line, context)
        context.cursor = self.line
        return context


class MoveCommand:
    def __init__(self, offset: LineOffset) -> None:
        self.offset = offset

    def __call__(self, context: Context) -> Context:
        line = context.cursor + self.offset
        raise_for_line_number(line, context)
        context.cursor = line
        return context


class InsertCommand:
    def __init__(self, input_string: str) -> None:
        self.input_string = input_string

    def __call__(self, context: Context) -> Context:
        if context.lines:
            input_lines = split_lines(self.input_string)
            lines_before, lines_after = split_lines_at_cursor(
                context.lines,
                context.cursor,
            )
            context.lines = lines_before + input_lines + lines_after
            context.cursor = len(lines_before) + len(input_lines)
            return context
        raise InvalidOperation("Cannot insert into an empty buffer")


class AppendCommand:
    def __init__(self, input_string: str) -> None:
        self.input_string = input_string

    def __call__(self, context: Context) -> Context:
        input_lines = split_lines(self.input_string)
        lines_before, lines_after = split_lines_at_cursor(
            context.lines,
            context.cursor + 1,
        )
        context.lines = lines_before + input_lines + lines_after
        context.cursor = len(lines_before) + len(input_lines)
        return context


class DeleteCommand:
    def __init__(self) -> None:
        self._range: tuple[LineNumber, LineNumber] | None = None

    def from_range(
        self,
        begin: LineNumber,
        end: LineNumber,
    ) -> "DeleteCommand":
        self._range = begin, end
        return self

    def __call__(self, context: Context) -> Context:
        if context.lines:
            if self._range:
                begin, end = self._range
                if begin > end:
                    raise InvalidOperation("The end range comes before begin.")

                raise_for_line_number(begin, context)
                raise_for_line_number(end, context)
                begin = to_index(begin)
                del context.lines[begin:end]
                context.cursor = to_line(begin)
                return context
            else:
                index = to_index(context.cursor)
                del context.lines[index]
            return context
        raise InvalidOperation("Cannot delete to an empty buffer.")


class SearchCommand:
    def __init__(self, input_regex: str) -> None:
        self._input_regex = input_regex
        self._pattern = re.compile(input_regex)
        self._reverse = False
        self._context: Context

    def in_reverse(self) -> "SearchCommand":
        self._reverse = True
        return self

    def __call__(self, context: Context) -> Context:
        self._context = context
        self._context.cursor = self._search_line()
        return self._context

    def _search_line(self) -> LineNumber:
        for line_number, line_text in self._make_lines_iterator():
            if self._match_pattern(line_text):
                return self._to_line_number(line_number)
        raise InvalidOperation("Pattern not found.")

    def _make_lines_iterator(self) -> Iterable[tuple[LineNumber, str]]:
        if self._reverse:
            return self._make_reverse_lines_iterator()
        else:
            return self._make_forward_lines_iterator()

    def _make_reverse_lines_iterator(self) -> Iterable[tuple[LineNumber, str]]:
        iterator = self._make_forward_lines_iterator()
        return reversed(list(iterator))

    def _make_forward_lines_iterator(self) -> Iterable[tuple[LineNumber, str]]:
        size = len(self._context.lines)
        cursor = self._context.cursor
        return enumerate(
            islice(cycle(self._context.lines), cursor, cursor + size),
            cursor,
        )

    def _match_pattern(self, line: str) -> bool:
        return bool(self._pattern.search(line))

    def _to_line_number(self, line: LineNumber) -> LineNumber:
        return line % len(self._context.lines)

    def _resolve_line(self, context: Context) -> LineNumber:
        self._context = context
        return self._search_line()


class SubstituteCommand:
    def __init__(self, search_regex: str, replace_regex: str) -> None:
        self._search_regex = search_regex
        self._replace_regex = replace_regex
        self._replace_times = 1
        self._pattern = re.compile(search_regex)

    def every_time(self) -> "SubstituteCommand":
        return self.times(0)

    def times(self, count: int) -> "SubstituteCommand":
        self._replace_times = count
        return self

    def __call__(self, context: Context) -> Context:
        index = to_index(context.cursor)
        line = context.lines[index]
        new_line, changes = self._pattern.subn(
            self._replace_regex,
            line,
            self._replace_times,
        )
        if changes > 0:
            context.lines[index] = new_line
            return context
        raise InvalidOperation("Substitute pattern not found.")


class CurrentLineResolver:
    def __init__(self, line: LineNumber) -> None:
        self.line = line

    def _resolve_line(self, context: Context) -> LineNumber:
        return self.line


def raise_for_line_number(line: LineNumber, context: Context) -> None:
    if 1 <= line <= len(context.lines):
        return
    raise InvalidOperation("The requested line does not exist.")


def split_lines_at_cursor(
    lines: list[str],
    cursor: LineNumber,
) -> tuple[list[str], list[str]]:
    pivot = to_index(cursor)
    return lines[:pivot], lines[pivot:]


def split_lines(input_string: str) -> list[str]:
    return [line + "\n" for line in input_string.splitlines()]


def to_line(index: LineIndex) -> LineNumber:
    return index + 1


def to_index(line: LineNumber) -> LineIndex:
    return line - 1
