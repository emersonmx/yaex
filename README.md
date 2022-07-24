# Yet Another EX command library

This is a library based on the ex command. So, it works the same way :)

## Usage

```python
from yaex import yaex, append, at_line, delete

result = yaex(
    append("Hello"),
    append("World"),
)
print(result, end="")
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
print(result, end="")
# >first line
# >third line
# >
```
