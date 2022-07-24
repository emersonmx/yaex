import pytest

from yaex import (
    InvalidOperation,
    append,
    at_first_line,
    at_last_line,
    at_line,
    delete,
    insert,
    read_string,
    yaex,
)


def test_should_return_an_empty_string_when_no_commands() -> None:
    buffer = yaex()
    assert buffer == ""


def test_should_raise_error_when_insert_into_an_empty_buffer() -> None:
    with pytest.raises(InvalidOperation):
        yaex(
            insert("Hello World"),
        )


def test_should_append_a_line_into_an_empty_buffer() -> None:
    buffer = yaex(
        append("Hello World"),
    )
    assert buffer == "Hello World\n"


def test_should_raise_error_when_delete_a_line_of_an_empty_buffer() -> None:
    with pytest.raises(InvalidOperation):
        yaex(
            delete(),
        )


def test_should_insert_a_line_after_an_append() -> None:
    buffer = yaex(
        append("Hello"),
        insert("World"),
    )
    assert buffer == "World\nHello\n"


def test_should_read_string() -> None:
    buffer = yaex(
        read_string("Hello World\n"),
    )
    assert buffer == "Hello World\n"


def test_should_insert_on_the_penultimate_line_by_default() -> None:
    expectd_buffer = (
        "first line\nsecond line\nthird line\nfourth line\nfifth line\n"
    )
    buffer = yaex(
        read_string("first line\nsecond line\nthird line\nfifth line\n"),
        insert("fourth line"),
    )
    assert buffer == expectd_buffer


def test_should_append_on_the_last_line_by_default() -> None:
    buffer = yaex(
        read_string("Hello\n"),
        append("World"),
    )
    assert buffer == "Hello\nWorld\n"


def test_should_delete_last_line_by_default() -> None:
    buffer = yaex(
        read_string("Hello\nWorld\n"),
        delete(),
    )
    assert buffer == "Hello\n"


def test_should_insert_on_the_first_line() -> None:
    buffer = yaex(
        read_string("second line\nthird line\n"),
        at_first_line(),
        insert("first line"),
    )
    assert buffer == "first line\nsecond line\nthird line\n"


def test_should_append_on_the_second_line() -> None:
    buffer = yaex(
        read_string("first line\nthird line\n"),
        at_first_line(),
        append("second line"),
    )
    assert buffer == "first line\nsecond line\nthird line\n"


def test_should_delete_the_first_line() -> None:
    buffer = yaex(
        read_string("Hello\nWorld\n"),
        at_first_line(),
        delete(),
    )
    assert buffer == "World\n"


def test_should_insert_on_the_penultimate_line() -> None:
    buffer = yaex(
        read_string("first line\nthird line\n"),
        at_last_line(),
        insert("second line"),
    )
    assert buffer == "first line\nsecond line\nthird line\n"


def test_should_append_on_the_last_line() -> None:
    buffer = yaex(
        read_string("first line\nsecond line\n"),
        at_last_line(),
        append("third line"),
    )
    assert buffer == "first line\nsecond line\nthird line\n"


def test_should_delete_last_line() -> None:
    buffer = yaex(
        read_string("first line\nsecond line\nthird line\n"),
        at_last_line(),
        delete(),
    )
    assert buffer == "first line\nsecond line\n"


def test_should_raise_error_when_move_the_cursor_to_an_invalid_line() -> None:
    input_text = (
        "first line\nsecond line\nthird line\nfourth line\nfifth line\n"
    )
    with pytest.raises(InvalidOperation):
        yaex(
            read_string(input_text),
            at_line(0),
        )
    with pytest.raises(InvalidOperation):
        yaex(
            read_string(input_text),
            at_line(6),
        )
    with pytest.raises(InvalidOperation):
        yaex(
            read_string(input_text),
            at_line(-1),
        )


def test_should_insert_at_any_line() -> None:
    buffer = yaex(
        read_string("first line\nsecond line\nfourth line\nfifth line\n"),
        at_line(3),
        insert("third line"),
    )
    assert (
        buffer
        == "first line\nsecond line\nthird line\nfourth line\nfifth line\n"
    )


def test_should_append_at_any_line() -> None:
    buffer = yaex(
        read_string("first line\nsecond line\nfourth line\nfifth line\n"),
        at_line(2),
        append("third line"),
    )
    assert (
        buffer
        == "first line\nsecond line\nthird line\nfourth line\nfifth line\n"
    )


def test_should_delete_any_line() -> None:
    buffer = yaex(
        read_string(
            "first line\nsecond line\nthird line\nfourth line\nfifth line\n",
        ),
        at_line(3),
        delete(),
    )
    assert buffer == "first line\nsecond line\nfourth line\nfifth line\n"


def test_should_move_cursor_when_append_a_line() -> None:
    buffer = yaex(
        append("first line"),
        append("second line"),
        append("third line"),
    )
    assert buffer == "first line\nsecond line\nthird line\n"
