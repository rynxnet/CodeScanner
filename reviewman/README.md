# ReviewMan - Comprehensive Code Review Assistant

ReviewMan is an AI-powered code review tool that combines quality, security, and performance analysis to help you maintain high-quality, secure code.

## Features

- **Security Analysis**: Detects vulnerabilities, hardcoded secrets, weak cryptography, and injection risks
- **Performance Checks**: Identifies inefficient patterns, expensive operations, and optimization opportunities
- **Code Quality**: Enforces style guidelines, detects code smells, and maintains consistency
- **Best Practices**: Ensures proper documentation, import structure, and exception handling
- **Multiple Output Formats**: Generate reports in text, JSON, or HTML format
- **Configurable**: Customize checks and thresholds via configuration files

## Installation

1. Make the script executable:
```bash
chmod +x reviewman.py
```

2. (Optional) Create a symlink for system-wide access:
```bash
sudo ln -s /path/to/reviewman/reviewman.py /usr/local/bin/reviewman
```

## Quick Start

### Review a single file:
```bash
./reviewman.py myfile.py
```

### Review a directory recursively:
```bash
./reviewman.py ./src --recursive
```

### Generate HTML report:
```bash
./reviewman.py ./src -r -f html -o report.html
```

### Use custom configuration:
```bash
./reviewman.py ./src -r --config myconfig.json
```

## Usage

```
reviewman.py [-h] [-r] [-c CONFIG] [-f {text,json,html}] [-o OUTPUT]
             [--no-security] [--no-performance] [--no-quality]
             path

Arguments:
  path                  File or directory to review

Options:
  -h, --help           Show help message
  -r, --recursive      Recursively review directories
  -c, --config CONFIG  Path to configuration file
  -f, --format FORMAT  Output format: text, json, or html (default: text)
  -o, --output FILE    Save report to file
  --no-security        Skip security checks
  --no-performance     Skip performance checks
  --no-quality         Skip quality checks
```

## Examples

### 1. Quick file review:
```bash
./reviewman.py app.py
```

### 2. Review entire project with HTML report:
```bash
./reviewman.py . -r -f html -o code_review_report.html
```

### 3. Security-focused review:
```bash
./reviewman.py ./src -r --no-quality --no-performance
```

### 4. Review with custom config:
```bash
./reviewman.py ./src -r -c config/strict_config.json
```

### 5. Save JSON report for CI/CD:
```bash
./reviewman.py ./src -r -f json -o review.json
```

## Configuration

Create a custom configuration file to adjust ReviewMan's behavior:

```json
{
  "max_line_length": 100,
  "max_function_length": 50,
  "check_security": true,
  "check_performance": true,
  "check_quality": true,
  "exclude_patterns": [
    "*.pyc",
    "__pycache__",
    ".git",
    "venv",
    "node_modules"
  ]
}
```

See `config/default_config.json` for all available options.

## Security Checks

ReviewMan detects:

- **Critical Issues**:
  - Use of `eval()` and `exec()`
  - Hardcoded passwords, API keys, and secrets
  - SQL injection vulnerabilities
  - Command injection via `shell=True`

- **High Severity**:
  - Unsafe pickle deserialization
  - Use of `os.system()`
  - Weak cryptography (MD5)
  - String formatting with user input

- **Medium Severity**:
  - Non-cryptographic random number generation
  - Unvalidated user input
  - Assert statements for validation

## Performance Checks

Identifies:

- Inefficient loop patterns (e.g., `range(len())`)
- String concatenation in loops
- Global variables
- Repeated API calls in loops
- Expensive operations that could be cached

## Quality Checks

Enforces:

- Line length limits
- Trailing whitespace removal
- TODO/FIXME comment tracking
- Print statement detection (suggests logging)
- Commented-out code removal

## Best Practices

Ensures:

- Proper docstring documentation
- No wildcard imports (`import *`)
- Specific exception handling (no bare `except:`)
- Reasonable file sizes
- Proper import organization

## Issue Severity Levels

- **Critical**: Immediate security risks or data exposure
- **High**: Significant vulnerabilities or performance problems
- **Medium**: Important issues that should be addressed
- **Low**: Minor improvements or style issues
- **Info**: Informational notes and suggestions

## Report Formats

### Text Format
Plain text report suitable for terminal viewing:
```
============================================================
REVIEWMAN - CODE REVIEW REPORT
============================================================
Generated: 2025-10-29 10:30:00

SUMMARY
Files Reviewed: 15
Lines Reviewed: 3,245
Total Issues Found: 42
```

### JSON Format
Machine-readable format for automation:
```json
{
  "findings": {
    "security": [...],
    "performance": [...],
    "quality": [...]
  },
  "stats": {
    "files_reviewed": 15,
    "lines_reviewed": 3245,
    "issues_found": 42
  }
}
```

### HTML Format
Beautiful, interactive web report with:
- Color-coded severity indicators
- Filterable issues by category
- Summary statistics dashboard
- Click-to-navigate file references

## Integration with CI/CD

### GitHub Actions
```yaml
- name: Run ReviewMan
  run: |
    python reviewman/reviewman.py ./src -r -f json -o review.json

- name: Check for critical issues
  run: |
    critical_count=$(jq '.findings.security | map(select(.severity=="critical")) | length' review.json)
    if [ "$critical_count" -gt 0 ]; then
      echo "Critical security issues found!"
      exit 1
    fi
```

### GitLab CI
```yaml
code_review:
  script:
    - python reviewman/reviewman.py ./src -r -f html -o review.html
  artifacts:
    paths:
      - review.html
    expire_in: 1 week
```

## Supported Languages

Currently supports:
- Python (.py)
- JavaScript (.js, .jsx)
- TypeScript (.ts, .tsx)
- Java (.java)
- C/C++ (.c, .cpp)
- Go (.go)
- Rust (.rs)
- Ruby (.rb)
- PHP (.php)

## Excluding Files/Directories

Add patterns to your config file:
```json
{
  "exclude_patterns": [
    "*.pyc",
    "__pycache__",
    ".git",
    "venv",
    "node_modules",
    "test_*.py",
    "vendor/*"
  ]
}
```

## Advanced Usage

### Custom Security Patterns

Extend the security checker by adding patterns in the source code:

```python
security_patterns = [
    (r'your_pattern', 'Your message', 'severity'),
    # Add your custom patterns here
]
```

### Pre-commit Hook

Add ReviewMan as a pre-commit hook:

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running ReviewMan..."
python reviewman/reviewman.py . -r --no-quality

if [ $? -ne 0 ]; then
    echo "Code review found issues. Commit aborted."
    exit 1
fi
```

## Performance

ReviewMan is designed to be fast:
- Processes ~1000 lines/second
- Minimal memory footprint
- Parallel processing support (coming soon)

## Contributing

Found a bug or want to add a feature? Contributions welcome!

1. Add new check patterns to the appropriate method
2. Update the configuration schema
3. Add tests for your changes
4. Update documentation

## Limitations

- Static analysis only (no runtime checks)
- Language-specific deep analysis requires specialized parsers
- False positives possible for complex patterns
- Context-aware analysis limited

## Roadmap

- [ ] Support for more languages
- [ ] AI-powered vulnerability detection
- [ ] Integration with vulnerability databases
- [ ] Automatic fix suggestions
- [ ] Real-time IDE integration
- [ ] Custom rule engine
- [ ] Team collaboration features
- [ ] Historical trend analysis

## License

MIT License - Use freely in your projects

## Support

For issues, questions, or suggestions:
- File an issue in the project repository
- Check the documentation
- Review existing issues for solutions

## Tips for Best Results

1. Run ReviewMan regularly during development
2. Fix critical and high severity issues immediately
3. Use custom configs for different project types
4. Integrate with your CI/CD pipeline
5. Review reports with your team
6. Keep the exclude patterns updated
7. Balance between strict and practical rules

## FAQ

**Q: How do I reduce false positives?**
A: Adjust severity thresholds in your config or disable specific checks that don't apply to your project.

**Q: Can I use this for production code?**
A: Yes! ReviewMan is designed for production use, but always review findings manually.

**Q: Does it replace human code review?**
A: No, it complements human review by catching common issues automatically.

**Q: How often should I run ReviewMan?**
A: Run it before commits, in CI/CD, and periodically on the entire codebase.

**Q: Can I add custom checks?**
A: Yes, modify the source code to add custom patterns and checks.

---

**ReviewMan** - Keep your code secure, performant, and high-quality!
