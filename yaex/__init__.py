from .commands import Command, Context
from .commands import DeleteCommand as delete
from .commands import InvalidOperation
from .commands import SearchCommand as search
from .commands import SubstituteCommand as substitute
from .commands import (
    append,
    go_to,
    go_to_first_line,
    go_to_last_line,
    insert,
    move,
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
    "substitute",
    "yaex",
]
