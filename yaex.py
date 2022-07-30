import re
from collections.abc import Callable
from dataclasses import dataclass
from itertools import cycle, islice


class InvalidOperation(Exception):
    pass


@dataclass
class Context:
    cursor: int
    lines: list[str]


Command = Callable[[Context], Context]


def yaex(*commands: Command) -> str:
    context = Context(cursor=0, lines=[])
    for command in commands:
        context = command(context)
    return "".join(context.lines)


def at_first_line() -> Command:
    def cmd(ctx: Context) -> Context:
        ctx.cursor = 0
        return ctx

    return cmd


def at_last_line() -> Command:
    def cmd(ctx: Context) -> Context:
        ctx.cursor = len(ctx.lines) - 1
        return ctx

    return cmd


def at_line(line: int) -> Command:
    def cmd(ctx: Context) -> Context:
        if 1 <= line <= len(ctx.lines):
            ctx.cursor = line - 1
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


def search(input_regex: str) -> Command:
    pattern = re.compile(input_regex)

    def cmd(ctx: Context) -> Context:
        size = len(ctx.lines)
        cursor = ctx.cursor
        lines_iterator = islice(cycle(ctx.lines), cursor, cursor + size)
        for i, line in enumerate(lines_iterator, start=cursor):
            if pattern.search(line):
                ctx.cursor = i % size
                return ctx
        raise InvalidOperation("Pattern not found.")

    return cmd
