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

## Examples

Using the file `loremipsum.txt` (provided in the repository) which contains:

```
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
```

- **Count lines**:  
  ```bash
  wordcount -l loremipsum.txt
  # Output: 4 loremipsum.txt
  ```

- **Count words**:  
  ```bash
  wordcount -w loremipsum.txt
  # Output: 69 loremipsum.txt
  ```

- **Count bytes**:  
  ```bash
  wordcount -c loremipsum.txt
  # Output: 446 loremipsum.txt
  ```

- **Count characters**:  
  ```bash
  wordcount -m loremipsum.txt
  # Output: 446 loremipsum.txt
  ```

- **Default behavior (lines, words, bytes)**:  
  ```bash
  wordcount loremipsum.txt
  # Output: 4 69 446 loremipsum.txt
  ```

- **Combine options (lines and characters)**:  
  ```bash
  wordcount -l -m loremipsum.txt
  # Output: 4 446 loremipsum.txt
  ```

- **From stdin**:  
  ```bash
  cat loremipsum.txt | wordcount
  # Output: 4 69 446
  ```

## Implementation Details

This tool was built using Python and the Typer library for the command-line interface.

## Differences from Unix `wc`

- This tool uses `-c` for bytes (like `wc`) and `-m` for characters (like `wc -m`).
- The default output shows lines, words, and bytes, matching `wc` default behavior.
- This tool does not implement the `-L`/`--max-line-length` option to print the length of the longest line.
