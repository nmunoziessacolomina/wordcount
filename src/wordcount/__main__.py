import sys
from typing import Optional, List, TextIO
import typer

app = typer.Typer()


def count_file(file: TextIO) -> tuple[int, int, int, int]:
    """
    Count lines, words, bytes, and characters in a file-like object.
    Returns a tuple (lines, words, bytes, chars).
    Bytes are counted as UTF-8 encoded bytes.
    Characters are counted as Unicode code points (len(line)).
    """
    lines = 0
    words = 0
    bytes_ = 0
    chars = 0
    for line in file:
        lines += 1
        words += len(line.split())
        bytes_ += len(line.encode('utf-8'))
        chars += len(line)
    return lines, words, bytes_, chars


def version_callback(value: bool):
    if value:
        try:
            from importlib.metadata import version
            ver = version("wordcount")
        except Exception:
            ver = "unknown"
        typer.echo(f"wordcount version {ver}")
        raise typer.Exit()


@app.command()
def main(
    files: List[typer.FileText] = typer.Argument(
        [], help="Files to read. If empty, reads from stdin."
    ),
    lines: bool = typer.Option(
        False, "-l", "--lines", help="Print the line count."
    ),
    words: bool = typer.Option(
        False, "-w", "--words", help="Print the word count."
    ),
    bytes_: bool = typer.Option(
        False, "-c", "--bytes", help="Print the byte count."
    ),
    chars: bool = typer.Option(
        False, "-m", "--chars", help="Print the character count."
    ),
    version: bool = typer.Option(
        None, "--version", callback=version_callback, is_eager=True, help="Show version and exit."
    ),
) -> None:
    """
    Count lines, words, bytes, and characters in FILEs, or from stdin if no FILE is given.
    """
    # If no option is specified, default to lines, words, bytes (like wc)
    if not (lines or words or bytes_ or chars):
        lines = words = bytes_ = True

    # If no files are provided, read from stdin
    if not files:
        files = [sys.stdin]

    total_lines = 0
    total_words = 0
    total_bytes = 0
    total_chars = 0

    for file in files:
        try:
            l, w, b, c = count_file(file)
        except Exception as e:
            typer.echo(f"Error reading {file.name}: {e}", err=True)
            raise typer.Exit(code=1)

        # Format output for this file
        output_parts = []
        if lines:
            output_parts.append(str(l))
        if words:
            output_parts.append(str(w))
        if bytes_:
            output_parts.append(str(b))
        if chars:
            output_parts.append(str(c))
        # If we are counting, we always output at least one field.
        output = " ".join(output_parts)
        # Print the filename if it's not stdin
        if file is not sys.stdin:
            output += f" {file.name}"
        typer.echo(output)

        # Accumulate totals if we are processing more than one file
        if len(files) > 1:
            total_lines += l
            total_words += w
            total_bytes += b
            total_chars += c

    # Print total if more than one file
    if len(files) > 1:
        total_parts = []
        if lines:
            total_parts.append(str(total_lines))
        if words:
            total_parts.append(str(total_words))
        if bytes_:
            total_parts.append(str(total_bytes))
        if chars:
            total_parts.append(str(total_chars))
        total_output = " ".join(total_parts)
        typer.echo(f"{total_output} total")


if __name__ == "__main__":
    app()