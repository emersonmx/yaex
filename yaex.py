from collections.abc import Callable
from dataclasses import dataclass


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


def insert(input_string: str) -> Command:
    def cmd(ctx: Context) -> Context:
        if ctx.lines:
            ctx.lines.insert(ctx.cursor, input_string + "\n")
            return ctx
        raise InvalidOperation("Cannot insert into an empty buffer")

    return cmd


def append(input_string: str) -> Command:
    def cmd(ctx: Context) -> Context:
        ctx.lines.insert(ctx.cursor + 1, input_string + "\n")
        return ctx

    return cmd


def delete() -> Command:
    def cmd(ctx: Context) -> Context:
        if ctx.lines:
            del ctx.lines[ctx.cursor]
            return ctx
        raise InvalidOperation("Cannot delete to an empty buffer.")

    return cmd


def read_string(input_string: str) -> Command:
    def cmd(ctx: Context) -> Context:
        new_lines = input_string.splitlines(keepends=True)
        ctx.cursor += len(new_lines) - 1
        ctx.lines += new_lines
        return ctx

    return cmd
