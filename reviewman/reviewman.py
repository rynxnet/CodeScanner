#!/usr/bin/env python3
"""
ReviewMan - Comprehensive Code Review Assistant
Combines quality, security, and performance analysis
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple
import re


class CodeReviewer:
    """Main code review orchestrator"""

    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.findings = {
            'quality': [],
            'security': [],
            'performance': [],
            'best_practices': []
        }
        self.stats = {
            'files_reviewed': 0,
            'lines_reviewed': 0,
            'issues_found': 0
        }

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from file or use defaults"""
        default_config = {
            'max_line_length': 100,
            'max_function_length': 50,
            'max_complexity': 10,
            'check_security': True,
            'check_performance': True,
            'check_quality': True,
            'exclude_patterns': ['*.pyc', '__pycache__', '.git', 'venv', 'node_modules'],
            'severity_levels': ['critical', 'high', 'medium', 'low', 'info']
        }

        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)

        return default_config

    def review_file(self, file_path: str) -> None:
        """Review a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')

            self.stats['files_reviewed'] += 1
            self.stats['lines_reviewed'] += len(lines)

            # Run different checks
            if self.config['check_quality']:
                self._check_code_quality(file_path, lines)

            if self.config['check_security']:
                self._check_security_issues(file_path, content, lines)

            if self.config['check_performance']:
                self._check_performance_issues(file_path, content, lines)

            self._check_best_practices(file_path, content, lines)

        except Exception as e:
            self._add_finding('quality', file_path, 0,
                            f"Error reading file: {str(e)}", 'high')

    def _check_code_quality(self, file_path: str, lines: List[str]) -> None:
        """Check code quality issues"""
        for i, line in enumerate(lines, 1):
            # Check line length
            if len(line) > self.config['max_line_length']:
                self._add_finding('quality', file_path, i,
                                f"Line exceeds {self.config['max_line_length']} characters ({len(line)})",
                                'low')

            # Check for TODO/FIXME comments
            if 'TODO' in line or 'FIXME' in line:
                self._add_finding('quality', file_path, i,
                                "TODO/FIXME comment found - should be addressed",
                                'info')

            # Check for trailing whitespace
            if line.endswith(' ') or line.endswith('\t'):
                self._add_finding('quality', file_path, i,
                                "Trailing whitespace detected",
                                'low')

            # Check for print statements (potential debug code)
            if re.search(r'^\s*print\s*\(', line) and not line.strip().startswith('#'):
                self._add_finding('quality', file_path, i,
                                "Print statement detected - use logging instead",
                                'medium')

            # Check for commented-out code
            stripped = line.strip()
            if stripped.startswith('#') and len(stripped) > 2:
                code_patterns = ['def ', 'class ', 'import ', 'if ', 'for ', 'while ']
                if any(pattern in stripped[1:] for pattern in code_patterns):
                    self._add_finding('quality', file_path, i,
                                    "Commented-out code detected - should be removed",
                                    'low')

    def _check_security_issues(self, file_path: str, content: str, lines: List[str]) -> None:
        """Check for security vulnerabilities"""
        security_patterns = [
            (r'eval\s*\(', 'Use of eval() is dangerous - arbitrary code execution risk', 'critical'),
            (r'exec\s*\(', 'Use of exec() is dangerous - arbitrary code execution risk', 'critical'),
            (r'pickle\.loads?\s*\(', 'Pickle deserialization can be unsafe - consider alternatives', 'high'),
            (r'subprocess\.call\([^)]*shell\s*=\s*True', 'Shell=True in subprocess is dangerous', 'critical'),
            (r'os\.system\s*\(', 'os.system() is vulnerable to command injection', 'high'),
            (r'password\s*=\s*["\']', 'Hardcoded password detected', 'critical'),
            (r'api[_-]?key\s*=\s*["\']', 'Hardcoded API key detected', 'critical'),
            (r'secret\s*=\s*["\']', 'Hardcoded secret detected', 'critical'),
            (r'md5\s*\(', 'MD5 is cryptographically broken - use SHA256 or better', 'high'),
            (r'random\.random\(\)', 'random.random() is not cryptographically secure - use secrets module', 'medium'),
            (r'input\s*\([^)]*\)', 'input() without validation can be dangerous', 'medium'),
            (r'\.format\s*\([^)]*request\.', 'String formatting with user input - SQL/command injection risk', 'high'),
            (r'SELECT\s+.*\s+.*\+\s*', 'Potential SQL injection - use parameterized queries', 'critical'),
            (r'assert\s+', 'Assert statements can be disabled - use proper validation', 'medium'),
        ]

        for i, line in enumerate(lines, 1):
            for pattern, message, severity in security_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    self._add_finding('security', file_path, i, message, severity)

        # Check for missing input validation
        if 'input(' in content and 'validate' not in content.lower():
            self._add_finding('security', file_path, 0,
                            "User input detected without apparent validation",
                            'medium')

    def _check_performance_issues(self, file_path: str, content: str, lines: List[str]) -> None:
        """Check for performance issues"""
        for i, line in enumerate(lines, 1):
            # Check for inefficient loops
            if re.search(r'for\s+\w+\s+in\s+range\s*\(\s*len\s*\(', line):
                self._add_finding('performance', file_path, i,
                                "Using range(len()) - consider enumerate() or direct iteration",
                                'low')

            # Check for string concatenation in loops
            if '+=' in line and 'str' in line.lower():
                self._add_finding('performance', file_path, i,
                                "String concatenation with += can be slow - consider join()",
                                'medium')

            # Check for global variables
            if re.match(r'^[A-Z_]+\s*=\s*', line) and not line.strip().startswith('#'):
                self._add_finding('performance', file_path, i,
                                "Global variable detected - can impact performance and testing",
                                'low')

            # Check for multiple API calls in loop
            if 'for ' in line or 'while ' in line:
                next_lines = lines[i:min(i+10, len(lines))]
                if any('requests.' in l or 'http' in l.lower() for l in next_lines):
                    self._add_finding('performance', file_path, i,
                                    "Potential API calls in loop - consider batch operations",
                                    'high')

    def _check_best_practices(self, file_path: str, content: str, lines: List[str]) -> None:
        """Check for best practice violations"""
        # Check for proper docstrings
        if file_path.endswith('.py'):
            if 'def ' in content and '"""' not in content:
                self._add_finding('best_practices', file_path, 0,
                                "Functions found without docstrings",
                                'medium')

            # Check for proper imports
            import_section = '\n'.join(lines[:50])  # Check first 50 lines
            if 'import *' in import_section:
                self._add_finding('best_practices', file_path, 0,
                                "Wildcard imports (import *) discouraged",
                                'medium')

        # Check for exception handling
        try_blocks = content.count('try:')
        bare_excepts = content.count('except:')
        if bare_excepts > 0:
            self._add_finding('best_practices', file_path, 0,
                            "Bare except clause found - specify exception types",
                            'medium')

        # Check file size
        if len(lines) > 500:
            self._add_finding('best_practices', file_path, 0,
                            f"Large file ({len(lines)} lines) - consider splitting",
                            'low')

    def _add_finding(self, category: str, file_path: str, line: int,
                    message: str, severity: str) -> None:
        """Add a finding to the results"""
        self.findings[category].append({
            'file': file_path,
            'line': line,
            'message': message,
            'severity': severity,
            'timestamp': datetime.now().isoformat()
        })
        self.stats['issues_found'] += 1

    def review_directory(self, directory: str, recursive: bool = True) -> None:
        """Review all files in a directory"""
        exclude_patterns = self.config['exclude_patterns']

        if recursive:
            for root, dirs, files in os.walk(directory):
                # Filter out excluded directories
                dirs[:] = [d for d in dirs if not any(
                    d == pattern.replace('*', '') for pattern in exclude_patterns
                )]

                for file in files:
                    if not any(file.endswith(pattern.replace('*', '')) for pattern in exclude_patterns):
                        file_path = os.path.join(root, file)
                        if self._should_review_file(file_path):
                            self.review_file(file_path)
        else:
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path) and self._should_review_file(file_path):
                    self.review_file(file_path)

    def _should_review_file(self, file_path: str) -> bool:
        """Determine if a file should be reviewed"""
        # Review text-based source code files
        reviewable_extensions = ['.py', '.js', '.java', '.c', '.cpp', '.go',
                                '.rs', '.rb', '.php', '.ts', '.jsx', '.tsx']
        return any(file_path.endswith(ext) for ext in reviewable_extensions)

    def generate_report(self, output_format: str = 'text') -> str:
        """Generate a review report"""
        if output_format == 'json':
            return json.dumps({
                'findings': self.findings,
                'stats': self.stats,
                'timestamp': datetime.now().isoformat()
            }, indent=2)

        elif output_format == 'html':
            return self._generate_html_report()

        else:  # text format
            return self._generate_text_report()

    def _generate_text_report(self) -> str:
        """Generate a plain text report"""
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("REVIEWMAN - CODE REVIEW REPORT")
        report_lines.append("=" * 80)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")

        # Summary statistics
        report_lines.append("SUMMARY")
        report_lines.append("-" * 80)
        report_lines.append(f"Files Reviewed: {self.stats['files_reviewed']}")
        report_lines.append(f"Lines Reviewed: {self.stats['lines_reviewed']}")
        report_lines.append(f"Total Issues Found: {self.stats['issues_found']}")
        report_lines.append("")

        # Severity breakdown
        severity_counts = {}
        for category in self.findings:
            for finding in self.findings[category]:
                severity = finding['severity']
                severity_counts[severity] = severity_counts.get(severity, 0) + 1

        report_lines.append("Issues by Severity:")
        for severity in ['critical', 'high', 'medium', 'low', 'info']:
            count = severity_counts.get(severity, 0)
            if count > 0:
                report_lines.append(f"  {severity.upper()}: {count}")
        report_lines.append("")

        # Detailed findings by category
        for category in ['security', 'performance', 'quality', 'best_practices']:
            if self.findings[category]:
                report_lines.append(f"\n{category.upper()} ISSUES ({len(self.findings[category])})")
                report_lines.append("-" * 80)

                # Sort by severity
                severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3, 'info': 4}
                sorted_findings = sorted(self.findings[category],
                                       key=lambda x: severity_order.get(x['severity'], 5))

                for finding in sorted_findings:
                    severity_marker = {
                        'critical': '[!!!]',
                        'high': '[!!]',
                        'medium': '[!]',
                        'low': '[-]',
                        'info': '[i]'
                    }.get(finding['severity'], '[?]')

                    report_lines.append(f"\n{severity_marker} {finding['severity'].upper()}")
                    report_lines.append(f"File: {finding['file']}")
                    if finding['line'] > 0:
                        report_lines.append(f"Line: {finding['line']}")
                    report_lines.append(f"Issue: {finding['message']}")

        report_lines.append("\n" + "=" * 80)
        report_lines.append("END OF REPORT")
        report_lines.append("=" * 80)

        return '\n'.join(report_lines)

    def _generate_html_report(self) -> str:
        """Generate an HTML report"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>ReviewMan - Code Review Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; }}
        h1 {{ color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
        h2 {{ color: #666; border-bottom: 2px solid #ddd; padding-bottom: 5px; }}
        .stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 20px 0; }}
        .stat-box {{ background: #f9f9f9; padding: 15px; border-left: 4px solid #4CAF50; }}
        .stat-label {{ color: #666; font-size: 14px; }}
        .stat-value {{ font-size: 24px; font-weight: bold; color: #333; }}
        .finding {{ margin: 15px 0; padding: 15px; border-radius: 5px; border-left: 4px solid #ddd; }}
        .critical {{ border-left-color: #f44336; background: #ffebee; }}
        .high {{ border-left-color: #ff9800; background: #fff3e0; }}
        .medium {{ border-left-color: #ffeb3b; background: #fffde7; }}
        .low {{ border-left-color: #2196f3; background: #e3f2fd; }}
        .info {{ border-left-color: #9e9e9e; background: #f5f5f5; }}
        .severity {{ display: inline-block; padding: 3px 8px; border-radius: 3px; font-size: 12px; font-weight: bold; color: white; }}
        .severity.critical {{ background: #f44336; }}
        .severity.high {{ background: #ff9800; }}
        .severity.medium {{ background: #ffeb3b; color: #333; }}
        .severity.low {{ background: #2196f3; }}
        .severity.info {{ background: #9e9e9e; }}
        .file {{ font-family: monospace; background: #eee; padding: 2px 5px; border-radius: 3px; }}
        .line {{ color: #666; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>ReviewMan - Code Review Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <div class="stats">
            <div class="stat-box">
                <div class="stat-label">Files Reviewed</div>
                <div class="stat-value">{self.stats['files_reviewed']}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Lines Reviewed</div>
                <div class="stat-value">{self.stats['lines_reviewed']:,}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Issues Found</div>
                <div class="stat-value">{self.stats['issues_found']}</div>
            </div>
        </div>
"""

        for category in ['security', 'performance', 'quality', 'best_practices']:
            if self.findings[category]:
                html += f"<h2>{category.upper()} ({len(self.findings[category])} issues)</h2>"

                severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3, 'info': 4}
                sorted_findings = sorted(self.findings[category],
                                       key=lambda x: severity_order.get(x['severity'], 5))

                for finding in sorted_findings:
                    html += f"""
                    <div class="finding {finding['severity']}">
                        <span class="severity {finding['severity']}">{finding['severity'].upper()}</span>
                        <br>
                        <span class="file">{finding['file']}</span>
                        """
                    if finding['line'] > 0:
                        html += f"""<span class="line"> (Line {finding['line']})</span>"""
                    html += f"""
                        <p><strong>{finding['message']}</strong></p>
                    </div>
                    """

        html += """
    </div>
</body>
</html>
"""
        return html

    def save_report(self, output_path: str, output_format: str = 'text') -> None:
        """Save the report to a file"""
        report = self.generate_report(output_format)

        with open(output_path, 'w') as f:
            f.write(report)

        print(f"Report saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='ReviewMan - Comprehensive Code Review Assistant',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  reviewman.py file.py                    # Review a single file
  reviewman.py ./src --recursive          # Review directory recursively
  reviewman.py ./src -f html -o report.html  # Generate HTML report
  reviewman.py ./src --config config.json # Use custom configuration
        """
    )

    parser.add_argument('path', help='File or directory to review')
    parser.add_argument('-r', '--recursive', action='store_true',
                       help='Recursively review directories')
    parser.add_argument('-c', '--config', help='Path to configuration file')
    parser.add_argument('-f', '--format', choices=['text', 'json', 'html'],
                       default='text', help='Output format (default: text)')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('--no-security', action='store_true',
                       help='Skip security checks')
    parser.add_argument('--no-performance', action='store_true',
                       help='Skip performance checks')
    parser.add_argument('--no-quality', action='store_true',
                       help='Skip quality checks')

    args = parser.parse_args()

    # Initialize reviewer
    reviewer = CodeReviewer(config_path=args.config)

    # Override config with command-line arguments
    if args.no_security:
        reviewer.config['check_security'] = False
    if args.no_performance:
        reviewer.config['check_performance'] = False
    if args.no_quality:
        reviewer.config['check_quality'] = False

    # Perform review
    if os.path.isfile(args.path):
        print(f"Reviewing file: {args.path}")
        reviewer.review_file(args.path)
    elif os.path.isdir(args.path):
        print(f"Reviewing directory: {args.path} (recursive: {args.recursive})")
        reviewer.review_directory(args.path, recursive=args.recursive)
    else:
        print(f"Error: Path not found: {args.path}")
        sys.exit(1)

    # Generate and output report
    if args.output:
        reviewer.save_report(args.output, output_format=args.format)
    else:
        print("\n" + reviewer.generate_report(output_format=args.format))


if __name__ == '__main__':
    main()
