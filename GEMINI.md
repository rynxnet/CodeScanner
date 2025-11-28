# Project Overview

This project, **ReviewMan**, is a command-line code review assistant written in Python. It is designed to analyze source code for security vulnerabilities, performance issues, code quality, and adherence to best practices. The tool can be run on individual files or entire directories, and it supports recursive scanning.

The main script, `reviewman/reviewman.py`, is self-contained and does not require external dependencies. It can generate reports in several formats, including plain text, JSON, and HTML. The analysis is configured through a JSON file (`reviewman/config/default_config.json`), which allows users to customize the checks and their parameters.

## Building and Running

### Running the Tool

As a Python script, there is no build process. The tool can be run directly using the Python 3 interpreter.

**Review a single file:**
```bash
python3 reviewman/reviewman.py <file_path>
```

**Review a directory recursively:**
```bash
python3 reviewman/reviewman.py <directory_path> -r
```

**Generate an HTML report:**
```bash
python3 reviewman/reviewman.py <path> -f html -o report.html
```

### Testing

There are no dedicated test files in the project. To test the tool's functionality, you can run it against a sample file or a project directory and inspect the output.

```bash
# Example of running on a sample file (if one exists)
python3 reviewman/reviewman.py sample_code.py
```

## Development Conventions

### Coding Style

The Python code in `reviewman/reviewman.py` follows standard Python conventions (PEP 8). It uses procedural programming with a central `CodeReviewer` class that orchestrates the analysis. The code is well-commented and includes type hints.

### Contribution Guidelines

The `GITHUB_SETUP.md` file provides instructions for setting up a Git repository and committing changes. While there is no formal `CONTRIBUTING.md`, the setup guide suggests a standard workflow of staging, committing, and pushing changes.

### Configuration

The tool's behavior is controlled by a JSON configuration file. This allows for a clean separation of the analysis logic from the configuration parameters. Key configurable options include:
- `max_line_length`
- `check_security`, `check_performance`, `check_quality`
- `exclude_patterns` for files and directories to ignore.
