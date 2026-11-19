from src.github.diff_parser import parse_diff


def test_parser_extracts_hunks_and_line_ranges() -> None:
    patch = (
        "@@ -10,2 +10,3 @@\n"
        " existing\n"
        "-removed\n"
        "+added\n"
        "+another\n"
    )

    result = parse_diff("src/example.py", "modified", patch)

    assert result.filename == "src/example.py"
    assert len(result.hunks) == 1
    assert result.hunks[0].start == 10
    assert result.hunks[0].end >= 10
