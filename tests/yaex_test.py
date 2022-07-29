from yaex import append, delete, insert, yaex


def test_should_return_an_empty_string_when_no_commands() -> None:
    buffer = yaex()
    assert buffer == ""


def test_should_insert_on_the_penultimate_line_by_default() -> None:
    expected_buffer = (
        "first line\nsecond line\nthird line\nfourth line\nfifth line\n"
    )
    buffer = yaex(
        append("first line\nsecond line\nthird line\nfifth line\n"),
        insert("fourth line"),
    )
    assert buffer == expected_buffer


def test_should_append_on_the_last_line_by_default() -> None:
    buffer = yaex(
        append("a line"),
        append("another line"),
    )
    assert buffer == "a line\nanother line\n"


def test_should_delete_last_line_by_default() -> None:
    buffer = yaex(
        append("a line\nanother line\n"),
        delete(),
    )
    assert buffer == "a line\n"
