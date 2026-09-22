import sys
from io import StringIO
from typer.testing import CliRunner

from wordcount.__main__ import app, count_file

runner = CliRunner()


def test_count_file():
    # Test with a simple string
    data = "Hello world\nThis is a test\n"
    file = StringIO(data)
    lines, words, bytes_, chars = count_file(file)
    assert lines == 2
    assert words == 6
    assert bytes_ == len(data.encode('utf-8'))
    assert chars == len(data)


def test_count_file_empty():
    file = StringIO("")
    lines, words, bytes_, chars = count_file(file)
    assert lines == 0
    assert words == 0
    assert bytes_ == 0
    assert chars == 0


def test_count_file_single_char():
    file = StringIO("a")
    lines, words, bytes_, chars = count_file(file)
    assert lines == 1
    assert words == 1
    assert bytes_ == len("a".encode('utf-8'))
    assert chars == 1


def test_count_file_newline_only():
    file = StringIO("\n")
    lines, words, bytes_, chars = count_file(file)
    assert lines == 1
    assert words == 0
    assert bytes_ == len("\n".encode('utf-8'))
    assert chars == 1


def test_cli_no_args_stdin():
    # Test stdin input via the input parameter
    result = runner.invoke(app, [], input="Hello world\nThis is a test\n")
    # Default behavior: lines, words, bytes (like wc)
    assert result.exit_code == 0
    # Output should be: "2 6 27" (bytes)
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


def test_cli_bytes_option():
    result = runner.invoke(app, ["-c"], input="Hello world\nThis is a test\n")
    assert result.exit_code == 0
    assert result.stdout.strip() == "27"


def test_cli_chars_option():
    result = runner.invoke(app, ["-m"], input="Hello world\nThis is a test\n")
    assert result.exit_code == 0
    assert result.stdout.strip() == "27"  # ASCII: bytes == chars


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
    # file1: 1 line, 2 words, 12 bytes
    # file2: 2 lines, 5 words, 23 bytes (including newlines: "This is a test\n"=15, "Goodbye\n"=8)
    # total: 3 lines, 7 words, 35 bytes
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

    result = runner.invoke(app, ["-l", "-w", "-m", "file1.txt", "file2.txt"])
    assert result.exit_code == 0
    lines = result.stdout.strip().split("\n")
    assert len(lines) == 3
    # file1: 1 line, 2 words, 12 chars
    # file2: 1 line, 4 words, 15 chars
    # total: 2 lines, 6 words, 27 chars
    assert lines[0] == "1 2 12 file1.txt"
    assert lines[1] == "1 4 15 file2.txt"
    assert lines[2] == "2 6 27 total"


def test_cli_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    # Output should start with "wordcount version"
    assert result.stdout.strip().startswith("wordcount version")