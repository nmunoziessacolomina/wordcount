# wordcount

A CLI tool inspired by Unix `wc` for counting lines, words, and characters.

## Features

- Count lines (`-l` or `--lines`)
- Count words (`-w` or `--words`)
- Count characters (`-c` or `--chars`)
- When no option is specified, defaults to showing lines, words, and characters.
- Accepts input from files specified on the command line or from stdin if no files are given.
- Supports multiple files and prints a total line.

## Installation

```bash
pip install .
```

## Usage

```bash
# Count lines, words, and characters from stdin
echo "Hello world" | wordcount

# Count lines in a file
wordcount -l file.txt

# Count words in multiple files
wordcount -w file1.txt file2.txt

# Count characters in multiple files with total
wordcount -c file1.txt file2.txt

# Default behavior (lines, words, characters)
wordcount file1.txt file2.txt
```

## Implementation Details

This tool was built using Python and the Typer library for the command-line interface.

## Differences from Unix `wc`

- This tool counts characters (Unicode code points) with `-c/--chars`, whereas Unix `wc` uses `-c` for bytes and `-m` for characters.
- The default output shows lines, words, and characters, while Unix `wc` shows lines, words, and bytes by default.
- This tool does not implement the `-L`/`--max-line-length` option to print the length of the longest line.