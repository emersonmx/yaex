import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from itertools import cycle, islice


class InvalidOperation(Exception):
    pass


@dataclass
class Context:
    cursor: int
    lines: list[str]


Command = Callable[[Context], Context]


def go_to_first_line() -> Command:
    def cmd(ctx: Context) -> Context:
        ctx.cursor = 0
        return ctx

    return cmd


def go_to_last_line() -> Command:
    def cmd(ctx: Context) -> Context:
        ctx.cursor = len(ctx.lines) - 1
        return ctx

    return cmd


def go_to(line: int) -> Command:
    def cmd(ctx: Context) -> Context:
        if 1 <= line <= len(ctx.lines):
            ctx.cursor = line - 1
            return ctx
        raise InvalidOperation("The requested line does not exist.")

    return cmd


def move(offset: int) -> Command:
    def cmd(ctx: Context) -> Context:
        line = ctx.cursor + offset
        if 0 <= line <= len(ctx.lines) - 1:
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
            cursor = ctx.cursor
            lines_before, lines_after = ctx.lines[:cursor], ctx.lines[cursor:]
            ctx.lines = lines_before + input_lines + lines_after
            ctx.cursor = len(lines_before) + len(input_lines) - 1
            return ctx
        raise InvalidOperation("Cannot insert into an empty buffer")

    return cmd


def append(input_string: str) -> Command:
    def cmd(ctx: Context) -> Context:
        input_lines = _split_lines(input_string)
        cursor = ctx.cursor + 1
        lines_before, lines_after = ctx.lines[:cursor], ctx.lines[cursor:]
        ctx.lines = lines_before + input_lines + lines_after
        ctx.cursor = len(lines_before) + len(input_lines) - 1
        return ctx

    return cmd


def delete() -> Command:
    def cmd(ctx: Context) -> Context:
        if ctx.lines:
            del ctx.lines[ctx.cursor]
            return ctx
        raise InvalidOperation("Cannot delete to an empty buffer.")

    return cmd


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
        lines_iterator: Iterable[tuple[int, str]] = enumerate(
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
        line = ctx.lines[ctx.cursor]
        new_line, changes = self._pattern.subn(
            self._replace_regex,
            line,
            self._replace_times,
        )
        if changes > 0:
            ctx.lines[ctx.cursor] = new_line
            return ctx
        raise InvalidOperation("Substitute pattern not found.")
