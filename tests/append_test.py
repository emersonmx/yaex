from yaex import Context, append


def test_should_append_a_line(empty_context: Context) -> None:
    command = append("a line")

    result = command(empty_context)

    assert result == Context(1, ["a line\n"])


def test_should_append_lines(empty_context: Context) -> None:
    command = append("a line")
    empty_context = command(empty_context)
    command = append("another line")
    result = command(empty_context)

    assert result == Context(2, ["a line\n", "another line\n"])


def test_should_append_lines_in_a_single_command(
    empty_context: Context,
) -> None:
    command = append("first line\nsecond line\nthird line\n")

    result = command(empty_context)

    assert result == Context(
        3,
        ["first line\n", "second line\n", "third line\n"],
    )


def test_should_append_lines_without_trailing_new_line(
    empty_context: Context,
) -> None:
    command = append("first line\nsecond line\nthird line")

    result = command(empty_context)

    assert result == Context(
        3,
        ["first line\n", "second line\n", "third line\n"],
    )


def test_should_append_between_lines(
    context: Context,
    lines: list[str],
) -> None:
    lines.insert(1, "---\n")
    command = append("---\n")

    result = command(context)

    assert result == Context(2, lines)
