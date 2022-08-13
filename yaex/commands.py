import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from itertools import cycle, islice


class InvalidOperation(Exception):
    pass


LineNumber = int
LineIndex = int
LineOffset = int


@dataclass
class Context:
    cursor: LineNumber
    lines: list[str]


Command = Callable[[Context], Context]


def go_to_first_line() -> Command:
    def cmd(ctx: Context) -> Context:
        ctx.cursor = 1
        return ctx

    return cmd


def go_to_last_line() -> Command:
    def cmd(ctx: Context) -> Context:
        ctx.cursor = len(ctx.lines)
        return ctx

    return cmd


def go_to(line: LineNumber) -> Command:
    def cmd(ctx: Context) -> Context:
        if 1 <= line <= len(ctx.lines):
            ctx.cursor = line
            return ctx
        raise InvalidOperation("The requested line does not exist.")

    return cmd


def move(offset: LineOffset) -> Command:
    def cmd(ctx: Context) -> Context:
        line = ctx.cursor + offset
        if 1 <= line <= len(ctx.lines):
            ctx.cursor = line
            return ctx
        raise InvalidOperation("The requested line does not exist.")

    return cmd


def _split_lines(input_string: str) -> list[str]:
    return [line + "\n" for line in input_string.splitlines()]


def insert(input_string: str) -> Command:
    def cmd(ctx: Context) -> Context:
        if ctx.lines:
            input_lines = _split_lines(input_string)
            pivot = to_index(ctx.cursor)
            lines_before, lines_after = ctx.lines[:pivot], ctx.lines[pivot:]
            ctx.lines = lines_before + input_lines + lines_after
            ctx.cursor = len(lines_before) + len(input_lines)
            return ctx
        raise InvalidOperation("Cannot insert into an empty buffer")

    return cmd


def append(input_string: str) -> Command:
    def cmd(ctx: Context) -> Context:
        input_lines = _split_lines(input_string)
        pivot = to_index(ctx.cursor + 1)
        lines_before, lines_after = ctx.lines[:pivot], ctx.lines[pivot:]
        ctx.lines = lines_before + input_lines + lines_after
        ctx.cursor = len(lines_before) + len(input_lines)
        return ctx

    return cmd


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

    def __call__(self, ctx: Context) -> Context:
        if ctx.lines:
            if self._range:
                begin, end = self._range
                if begin > end:
                    raise InvalidOperation("The end range comes before begin.")

                size = len(ctx.lines)
                if (1 <= begin <= size) and (1 <= end <= size):
                    begin = to_index(begin)
                    del ctx.lines[begin:end]
                    ctx.cursor = to_line(begin)
                    return ctx
                raise InvalidOperation(
                    f"The range is not between 1 and {size}.",
                )
            else:
                index = to_index(ctx.cursor)
                del ctx.lines[index]
            return ctx
        raise InvalidOperation("Cannot delete to an empty buffer.")


class SearchCommand:
    def __init__(self, input_regex: str) -> None:
        self._input_regex = input_regex
        self._pattern = re.compile(input_regex)
        self._reverse = False

    def in_reverse(self) -> "SearchCommand":
        self._reverse = True
        return self

    def __call__(self, ctx: Context) -> Context:
        size = len(ctx.lines)
        cursor = ctx.cursor
        lines_iterator: Iterable[tuple[LineNumber, str]] = enumerate(
            islice(cycle(ctx.lines), cursor, cursor + size),
            cursor,
        )
        if self._reverse:
            lines_iterator = reversed(list(lines_iterator))
        for i, line in lines_iterator:
            if self._pattern.search(line):
                ctx.cursor = i % size
                return ctx
        raise InvalidOperation("Pattern not found.")


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

    def __call__(self, ctx: Context) -> Context:
        index = to_index(ctx.cursor)
        line = ctx.lines[index]
        new_line, changes = self._pattern.subn(
            self._replace_regex,
            line,
            self._replace_times,
        )
        if changes > 0:
            ctx.lines[index] = new_line
            return ctx
        raise InvalidOperation("Substitute pattern not found.")


def to_line(index: LineIndex) -> LineNumber:
    return index + 1


def to_index(line: LineNumber) -> LineIndex:
    return line - 1
