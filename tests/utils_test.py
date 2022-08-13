from yaex.commands import to_index, to_line


def test_should_convert_a_line_index_to_line_number() -> None:
    assert to_line(-1) == 0
    assert to_line(0) == 1
    assert to_line(1) == 2


def test_should_convert_a_line_number_to_line_index() -> None:
    assert to_index(0) == -1
    assert to_index(1) == 0
    assert to_index(2) == 1
