import subprocess
import sys

import pytest

from app.wordstat.wordstat import count_words


def test_counts_repeated_words(tmp_path):
    file = tmp_path / "sample.txt"
    file.write_text("apple banana apple", encoding="utf-8")

    result = count_words(file)

    assert result["apple"] == 2
    assert result["banana"] == 1


def test_top_n_limits_results(tmp_path):
    file = tmp_path / "sample.txt"
    file.write_text("apple apple banana orange", encoding="utf-8")

    result = count_words(file)

    assert len(result.most_common(2)) == 2
    assert result.most_common(2) == [("apple", 2), ("banana", 1)]


def test_empty_file(tmp_path):
    file = tmp_path / "empty.txt"
    file.write_text("", encoding="utf-8")

    result = count_words(file)

    assert result == {}


def test_missing_file(tmp_path):
    file = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError, match="File not found"):
        count_words(file)


def test_unicode_words(tmp_path):
    file = tmp_path / "unicode.txt"
    file.write_text("café café naïve", encoding="utf-8")

    result = count_words(file)

    assert result["café"] == 2
    assert result["naïve"] == 1


def test_very_long_line(tmp_path):
    file = tmp_path / "long.txt"
    file.write_text(("apple " * 100_000) + "banana", encoding="utf-8")

    result = count_words(file)

    assert result["apple"] == 100_000
    assert result["banana"] == 1


def test_words_are_case_insensitive(tmp_path):
    file = tmp_path / "case.txt"
    file.write_text("Hello hello HELLO", encoding="utf-8")

    result = count_words(file)

    assert result["hello"] == 3


def test_punctuation_is_ignored(tmp_path):
    file = tmp_path / "punctuation.txt"
    file.write_text("hello, hello! world.", encoding="utf-8")

    result = count_words(file)

    assert result["hello"] == 2
    assert result["world"] == 1


def test_cli_missing_file_shows_error():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "app.wordstat.wordstat",
            "does_not_exist.txt",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "File not found" in result.stderr
