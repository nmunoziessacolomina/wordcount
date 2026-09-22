import sys
from io import StringIO
from typer.testing import CliRunner

from wordcount.__main__ import app, count_file

runner = CliRunner()


def test_count_file():
    # Test with a simple string
    data = "Hello world\nThis is a test\n"
    file = StringIO(data)
    lines, words, chars = count_file(file)
    assert lines == 2
    assert words == 6
    assert chars == len(data)


def test_count_file_empty():
    file = StringIO("")
    lines, words, chars = count_file(file)
    assert lines == 0
    assert words == 0
    assert chars == 0


def test_count_file_single_char():
    file = StringIO("a")
    lines, words, chars = count_file(file)
    assert lines == 1
    assert words == 1
    assert chars == 1


def test_count_file_newline_only():
    file = StringIO("\n")
    lines, words, chars = count_file(file)
    assert lines == 1
    assert words == 0
    assert chars == 1


def test_cli_no_args_stdin():
    # Test stdin input via the input parameter
    result = runner.invoke(app, [], input="Hello world\nThis is a test\n")
    # Default behavior: lines, words, chars
    assert result.exit_code == 0
    # Output should be: "2 6 27" (note: newline characters count)
    # Let's compute: "Hello world\n" -> 12 chars, "This is a test\n" -> 15 chars, total 27? Wait, let's count:
    # Actually, we have two lines:
    # Line1: "Hello world\n" -> 12 (H e l l o   w o r l d \n)
    # Line2: "This is a test\n" -> 15 (T h i s   i s   a   t e s t \n)
    # Total: 27 characters.
    # But our count_file counts the newline as part of the line, so yes.
    # Expected output: "2 6 27"
    output = result.stdout.strip()
    assert output == "2 6 27"


def test_cli_lines_option():
    result = runner.invoke(app, ["-l"], input="Hello world\nThis is a test\n")
    assert result.exit_code == 0
    assert result.stdout.strip() == "2"


def test_cli_words_option():
    result = runner.invoke(app, ["-w"], input="Hello world\nThis is a test\n")
    assert result.exit_code == 0
    assert result.stdout.strip() == "6"


def test_cli_chars_option():
    result = runner.invoke(app, ["-c"], input="Hello world\nThis is a test\n")
    assert result.exit_code == 0
    assert result.stdout.strip() == "27"


def test_cli_multiple_files(tmp_path, monkeypatch):
    # Create two temporary files
    file1 = tmp_path / "file1.txt"
    file1.write_text("Hello world\n")
    file2 = tmp_path / "file2.txt"
    file2.write_text("This is a test\nGoodbye\n")
    # Change to the temporary directory so that file paths are relative
    monkeypatch.chdir(tmp_path)

    # Invoke with both files
    result = runner.invoke(app, ["file1.txt", "file2.txt"])
    assert result.exit_code == 0
    # Expected output:
    # file1: 1 line, 2 words, 12 chars
    # file2: 2 lines, 5 words, 23 chars (including newlines: "This is a test\n"=15, "Goodbye\n"=8)
    # total: 3 lines, 7 words, 35 chars
    # Format:
    #   1 2 12 file1.txt
    #   2 5 23 file2.txt
    #   3 7 35 total
    lines = result.stdout.strip().split("\n")
    assert len(lines) == 3
    assert lines[0] == "1 2 12 file1.txt"
    assert lines[1] == "2 5 23 file2.txt"
    assert lines[2] == "3 7 35 total"


def test_cli_multiple_files_with_options(tmp_path, monkeypatch):
    file1 = tmp_path / "file1.txt"
    file1.write_text("Hello world\n")
    file2 = tmp_path / "file2.txt"
    file2.write_text("This is a test\n")
    # Change to the temporary directory so that file paths are relative
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["-l", "-w", "file1.txt", "file2.txt"])
    assert result.exit_code == 0
    lines = result.stdout.strip().split("\n")
    assert len(lines) == 3
    # file1: 1 line, 2 words
    # file2: 1 line, 4 words
    # total: 2 lines, 6 words
    assert lines[0] == "1 2 file1.txt"
    assert lines[1] == "1 4 file2.txt"
    assert lines[2] == "2 6 total"