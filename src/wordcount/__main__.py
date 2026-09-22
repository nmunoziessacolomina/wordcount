import sys
from typing import Optional, List, TextIO
import typer

app = typer.Typer()


def count_file(file: TextIO) -> tuple[int, int, int]:
    """
    Count lines, words, and characters in a file-like object.
    Returns a tuple (lines, words, chars).
    """
    lines = 0
    words = 0
    chars = 0
    for line in file:
        lines += 1
        words += len(line.split())
        chars += len(line)
    return lines, words, chars


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
    chars: bool = typer.Option(
        False, "-c", "--chars", help="Print the character count."
    ),
) -> None:
    """
    Count lines, words, and characters in FILEs, or from stdin if no FILE is given.
    """
    typer.echo("DEBUG: main called", err=True)
    # If no option is specified, default to all three
    if not (lines or words or chars):
        lines = words = chars = True

    # If no files are provided, read from stdin
    if not files:
        files = [sys.stdin]

    total_lines = 0
    total_words = 0
    total_chars = 0

    for file in files:
        # If the file is stdin, we need to reset the pointer? Actually, we just read it.
        # But note: if we are going to read multiple files and one of them is stdin,
        # we can only read stdin once. However, the typical wc behavior is to read
        # either multiple files or stdin, not a mix. We'll follow that: if stdin is
        # provided along with other files, we treat it as one of the files (and can
        # only read it once). This is acceptable.
        typer.echo(f"DEBUG: file={file}, name={getattr(file, 'name', 'no name')}", err=True)
        typer.echo(f"DEBUG: file id={id(file)}", err=True)
        typer.echo(f"DEBUG: sys module id={id(sys)}", err=True)
        typer.echo(f"DEBUG: sys.stdin id={id(sys.stdin)}", err=True)
        if hasattr(file, "getvalue"):
            typer.echo(f"DEBUG: file content={file.getvalue()!r}", err=True)
        elif hasattr(file, "tell") and hasattr(file, "seek"):
            pos = file.tell()
            file.seek(0)
            preview = file.read(20)
            file.seek(pos)
            typer.echo(f"DEBUG: preview={preview!r}", err=True)
        else:
            typer.echo(f"DEBUG: file not seekable", err=True)
        try:
            l, w, c = count_file(file)
        except Exception as e:
            typer.echo(f"Error reading {file.name}: {e}", err=True)
            raise typer.Exit(code=1)

        # Format output for this file
        output_parts = []
        if lines:
            output_parts.append(str(l))
        if words:
            output_parts.append(str(w))
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
            total_chars += c

    # Print total if more than one file
    if len(files) > 1:
        total_parts = []
        if lines:
            total_parts.append(str(total_lines))
        if words:
            total_parts.append(str(total_words))
        if chars:
            total_parts.append(str(total_chars))
        total_output = " ".join(total_parts)
        typer.echo(f"{total_output} total")


if __name__ == "__main__":
    app()