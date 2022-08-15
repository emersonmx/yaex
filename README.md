# Yet Another EX command library

This is a library based on the ex command. So, it works the same way :)

## Usage

```python
from yaex import *

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
    go_to(2),
    delete(),
)
print(result)
# >first line
# >third line
# >

result = yaex(
    append("# yaex\n\nThis is a library based on the ex command.\n"),
    go_to_first_line(),
    delete(),
    insert("# Yet Another EX command library"),
)
print(result)
# ># Yet Another EX command library
# >
# >This is a library based on the ex command.
# >

result = yaex(
    append("first line\nsecond line\nthird line\nfourth line\nfifth line\nsixth line\n"),
    delete().from_range(search("second"), search("fifth")),
)
print(result)
# >first line
# >sixth line
# >

result = yaex(
    append("first line\nsecond line\nthird line\nfourth line\nfifth line\nsixth line\n"),
    substitute("line", "LINE").from_range(go_to_first_line(), go_to_last_line()),
)
print(result)
# >first LINE
# >second LINE
# >third LINE
# >fourth LINE
# >fifth LINE
# >sixth LINE
# >
```
