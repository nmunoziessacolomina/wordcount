# wordcount

A CLI tool inspired by Unix `wc` for counting lines, words, bytes, and characters.

## Features

- Count lines (`-l` or `--lines`)
- Count words (`-w` or `--words`)
- Count bytes (`-c` or `--bytes`)
- Count characters (`-m` or `--chars`)
- When no option is specified, defaults to showing lines, words, and bytes (like `wc`).
- Accepts input from files specified on the command line or from stdin if no files are given.
- Supports multiple files and prints a total line.
- Version information with `--version`.

## Installation

```bash
pip install .
```

## Usage

```bash
# Count lines, words, and bytes from stdin (default)
echo "Hello world" | wordcount

# Count lines in a file
wordcount -l file.txt

# Count words in multiple files
wordcount -w file1.txt file2.txt

# Count bytes in multiple files with total
wordcount -c file1.txt file2.txt

# Count characters in multiple files with total
wordcount -m file1.txt file2.txt

# Default behavior (lines, words, bytes)
wordcount file1.txt file2.txt

# Show version
wordcount --version
```

## Implementation Details

This tool was built using Python and the Typer library for the command-line interface.

## Differences from Unix `wc`

- This tool uses `-c` for bytes (like `wc`) and `-m` for characters (like `wc -m`).
- The default output shows lines, words, and bytes, matching `wc` default behavior.
- This tool does not implement the `-L`/`--max-line-length` option to print the length of the longest line.