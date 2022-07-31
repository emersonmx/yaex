from .commands import (
    Command,
    Context,
    InvalidOperation,
    append,
    delete,
    go_to,
    go_to_first_line,
    go_to_last_line,
    insert,
    move,
    search,
)


def yaex(*commands: Command) -> str:
    context = Context(cursor=0, lines=[])
    for command in commands:
        context = command(context)
    return "".join(context.lines)


__all__ = [
    "Command",
    "Context",
    "InvalidOperation",
    "append",
    "delete",
    "go_to",
    "go_to_first_line",
    "go_to_last_line",
    "insert",
    "move",
    "search",
    "yaex",
]
