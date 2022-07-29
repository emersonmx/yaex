# Yet Another EX command library

This is a library based on the ex command. So, it works the same way :)

## Usage

```python
from yaex import append, at_first_line, at_line, delete, insert, yaex

result = yaex(
    append("Hello"),
    append("World"),
)
print(result)
# >Hello
# >World
# >

result = yaex(
    append("first line"),
    append("second line"),
    append("third line"),
    at_line(2),
    delete(),
)
print(result)
# >first line
# >third line
# >

result = yaex(
    append("# yaex\n\nThis is a library based on the ex command.\n"),
    at_first_line(),
    delete(),
    insert("# Yet Another EX command library"),
)
print(result)
# ># Yet Another EX command library
# >
# >This is a library based on the ex command.
# >
```
