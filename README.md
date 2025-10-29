# ReviewMan - AI-Powered Code Review Assistant

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

**ReviewMan** is a comprehensive, intelligent code review tool that combines security analysis, performance optimization, and quality enforcement to help you maintain clean, secure, and high-performing code.

## Overview

ReviewMan automatically scans your codebase to detect:
- 🔒 **Security Vulnerabilities** - SQL injection, hardcoded secrets, command injection
- ⚡ **Performance Issues** - Inefficient loops, expensive operations, optimization opportunities
- ✨ **Code Quality** - Style violations, code smells, maintainability issues
- 📚 **Best Practices** - Documentation, proper imports, exception handling

## Features

### Security Analysis
- Detects hardcoded passwords, API keys, and secrets
- Identifies SQL and command injection vulnerabilities
- Flags dangerous functions (`eval()`, `exec()`, `os.system()`)
- Checks for weak cryptography (MD5, insecure random)
- Validates input handling and sanitization

### Performance Optimization
- Identifies inefficient loop patterns
- Detects string concatenation issues
- Flags global variables
- Spots repeated API calls in loops
- Suggests caching opportunities

### Code Quality
- Enforces line length limits
- Detects trailing whitespace
- Tracks TODO/FIXME comments
- Identifies print statements (suggests logging)
- Finds commented-out code

### Best Practices
- Ensures proper documentation
- Checks import organization
- Validates exception handling
- Monitors file size
- Enforces coding standards

### Multiple Output Formats
- **Text** - Terminal-friendly plain text reports
- **JSON** - Machine-readable for CI/CD integration
- **HTML** - Beautiful, interactive web reports

## Installation

### Prerequisites
- Python 3.8 or higher
- No external dependencies required (uses Python standard library)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/yourusername/ReviewMan.git

# Navigate to the directory
cd ReviewMan

# Make the script executable
chmod +x reviewman/reviewman.py

# (Optional) Create a symlink for system-wide access
sudo ln -s $(pwd)/reviewman/reviewman.py /usr/local/bin/reviewman
```

## Quick Start

### Basic Usage

```bash
# Review a single file
python3 reviewman/reviewman.py myfile.py

# Review entire project recursively
python3 reviewman/reviewman.py . -r

# Generate HTML report
python3 reviewman/reviewman.py . -r -f html -o report.html

# Security-focused scan
python3 reviewman/reviewman.py . -r --no-quality --no-performance
```

### Command-Line Options

```
usage: reviewman.py [-h] [-r] [-c CONFIG] [-f {text,json,html}] [-o OUTPUT]
                    [--no-security] [--no-performance] [--no-quality]
                    path

positional arguments:
  path                  File or directory to review

options:
  -h, --help           Show help message
  -r, --recursive      Recursively review directories
  -c, --config CONFIG  Path to configuration file
  -f, --format FORMAT  Output format: text, json, or html
  -o, --output FILE    Save report to file
  --no-security        Skip security checks
  --no-performance     Skip performance checks
  --no-quality         Skip quality checks
```

## Examples

### Example 1: Quick File Review
```bash
python3 reviewman/reviewman.py app.py
```

### Example 2: Full Project Review with HTML Report
```bash
python3 reviewman/reviewman.py . -r -f html -o code_review.html
```

### Example 3: Security Audit Only
```bash
python3 reviewman/reviewman.py ./src -r --no-quality --no-performance -o security_audit.txt
```

### Example 4: CI/CD Integration (JSON Output)
```bash
python3 reviewman/reviewman.py . -r -f json -o review.json
```

## Configuration

Customize ReviewMan's behavior with a configuration file:

```json
{
  "max_line_length": 100,
  "max_function_length": 50,
  "max_complexity": 10,
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

Use your custom config:
```bash
python3 reviewman/reviewman.py . -r --config myconfig.json
```

## Severity Levels

ReviewMan categorizes issues by severity:

| Severity | Description | Action |
|----------|-------------|--------|
| 🔴 **CRITICAL** | Immediate security risks, data exposure | Fix immediately |
| 🟠 **HIGH** | Significant vulnerabilities, major issues | Fix soon |
| 🟡 **MEDIUM** | Important improvements needed | Should address |
| 🔵 **LOW** | Minor issues, style violations | Nice to fix |
| ⚪ **INFO** | Informational notes, suggestions | Optional |

## Supported Languages

- Python (.py)
- JavaScript (.js, .jsx)
- TypeScript (.ts, .tsx)
- Java (.java)
- C/C++ (.c, .cpp)
- Go (.go)
- Rust (.rs)
- Ruby (.rb)
- PHP (.php)

## CI/CD Integration

### GitHub Actions

```yaml
name: Code Review

on: [push, pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Run ReviewMan
        run: |
          python3 reviewman/reviewman.py . -r -f json -o review.json

      - name: Check for critical issues
        run: |
          critical=$(jq '.findings.security | map(select(.severity=="critical")) | length' review.json)
          if [ "$critical" -gt 0 ]; then
            echo "Critical security issues found!"
            exit 1
          fi

      - name: Upload report
        uses: actions/upload-artifact@v2
        with:
          name: code-review-report
          path: review.json
```

### GitLab CI

```yaml
code_review:
  stage: test
  script:
    - python3 reviewman/reviewman.py . -r -f html -o review.html
  artifacts:
    paths:
      - review.html
    expire_in: 1 week
```

## Project Structure

```
ReviewGIT/
├── README.md                          # This file
├── Instructions.txt                   # Quick reference guide
├── guide.txt                          # AI/Cybersecurity project guide
└── reviewman/
    ├── reviewman.py                   # Main script
    ├── README.md                      # Detailed documentation
    ├── config/
    │   └── default_config.json       # Default configuration
    ├── checks/                        # Check modules (future)
    └── reports/                       # Report templates (future)
```

## Use Cases

### Before Committing
```bash
python3 reviewman/reviewman.py . -r
```

### Pre-deployment Security Audit
```bash
python3 reviewman/reviewman.py . -r --no-quality -o security_check.txt
```

### Code Quality Review
```bash
python3 reviewman/reviewman.py ./src -r -f html -o quality_report.html
```

### Weekly Team Review
```bash
python3 reviewman/reviewman.py . -r -f html -o team_review_$(date +%Y%m%d).html
```

## Sample Output

```
================================================================================
REVIEWMAN - CODE REVIEW REPORT
================================================================================
Generated: 2025-10-29 10:30:00

SUMMARY
--------------------------------------------------------------------------------
Files Reviewed: 15
Lines Reviewed: 3,245
Total Issues Found: 42

Issues by Severity:
  CRITICAL: 2
  HIGH: 5
  MEDIUM: 15
  LOW: 18
  INFO: 2

SECURITY ISSUES (7)
--------------------------------------------------------------------------------
[!!!] CRITICAL
File: app.py
Line: 45
Issue: Hardcoded API key detected
```

## Performance

- Processes ~1,000 lines/second
- Minimal memory footprint
- Suitable for large codebases
- No external API calls (fully offline)

## Roadmap

- [ ] Support for more programming languages
- [ ] AI-powered vulnerability detection
- [ ] Custom rule engine
- [ ] IDE integration (VS Code, PyCharm)
- [ ] Real-time code analysis
- [ ] Team collaboration features
- [ ] Historical trend analysis
- [ ] Automatic fix suggestions

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Adding New Checks

To add custom security patterns or checks:

```python
# In reviewman.py, add to security_patterns list:
security_patterns = [
    (r'your_regex_pattern', 'Your warning message', 'severity'),
    # Add your patterns here
]
```

## FAQ

**Q: Does ReviewMan replace human code review?**
A: No, it complements human review by automatically catching common issues.

**Q: Can I use this in production?**
A: Yes! ReviewMan is designed for production use.

**Q: How do I reduce false positives?**
A: Adjust severity thresholds in your config or disable specific checks.

**Q: Does it send my code anywhere?**
A: No, ReviewMan runs completely offline on your local machine.

**Q: Can I add custom rules?**
A: Yes, you can modify the source code to add custom patterns and checks.

## License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2025 ReviewMan Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Support

- 📧 Issues: [GitHub Issues](https://github.com/yourusername/ReviewMan/issues)
- 📖 Documentation: See `reviewman/README.md` and `Instructions.txt`
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/ReviewMan/discussions)

## Acknowledgments

- Inspired by the need for accessible, offline code review tools
- Built for developers who care about security and code quality
- Community-driven development

## Related Projects

This repository also includes:
- **guide.txt** - Comprehensive AI & Cybersecurity project guide
- **Instructions.txt** - Quick command reference for ReviewMan

---

**Made with ❤️ by developers, for developers**

⭐ Star this repo if you find it useful!

🐛 Found a bug? [Open an issue](https://github.com/yourusername/ReviewMan/issues)

🤝 Want to contribute? [Check our guidelines](#contributing)
