from yaex import Context, append


def make_context() -> Context:
    return Context(0, [])


def test_should_append_a_line() -> None:
    context = make_context()
    command = append("a line")

    result = command(context)

    assert result == Context(0, ["a line\n"])


def test_should_append_lines() -> None:
    context = make_context()

    command = append("a line")
    context = command(context)
    command = append("another line")
    result = command(context)

    assert result == Context(1, ["a line\n", "another line\n"])


def test_should_append_lines_in_a_single_command() -> None:
    context = make_context()
    command = append("first line\nsecond line\nthird line\n")

    result = command(context)

    assert result == Context(
        2,
        ["first line\n", "second line\n", "third line\n"],
    )


def test_should_append_lines_without_trailing_new_line() -> None:
    context = make_context()
    command = append("first line\nsecond line\nthird line")

    result = command(context)

    assert result == Context(
        2,
        ["first line\n", "second line\n", "third line\n"],
    )


def test_should_append_between_lines() -> None:
    context = Context(0, ["first line\n", "third line\n"])
    command = append("second line\n")

    result = command(context)

    assert result == Context(
        1,
        ["first line\n", "second line\n", "third line\n"],
    )
