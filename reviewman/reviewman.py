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


from reviewman.checks import (
    check_code_quality,
    check_security_issues,
    check_performance_issues,
    check_best_practices
)
from reviewman.reports import (
    generate_html_report,
    generate_json_report,
    generate_text_report
)


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
        default_config_path = os.path.join(os.path.dirname(__file__), 'config', 'default_config.json')
        with open(default_config_path, 'r') as f:
            default_config = json.load(f)

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
            if self.config.get('check_quality', False):
                for finding in check_code_quality(file_path, lines, self.config):
                    self._add_finding(finding['category'], finding['file_path'], finding['line'], finding['message'], finding['severity'])

            if self.config.get('check_security', False):
                for finding in check_security_issues(file_path, content, lines, self.config):
                    self._add_finding(finding['category'], finding['file_path'], finding['line'], finding['message'], finding['severity'])

            if self.config.get('check_performance', False):
                for finding in check_performance_issues(file_path, content, lines, self.config):
                    self._add_finding(finding['category'], finding['file_path'], finding['line'], finding['message'], finding['severity'])

            for finding in check_best_practices(file_path, content, lines, self.config):
                self._add_finding(finding['category'], finding['file_path'], finding['line'], finding['message'], finding['severity'])

        except Exception as e:
            self._add_finding('quality', file_path, 0,
                            f"Error reading file: {str(e)}", 'high')

    def _add_finding(self, category: str, file_path: str, line: int,
                    message: str, severity: str) -> None:
        """Add a finding to the results"""
        self.findings[category].append({
            'file_path': file_path,
            'line': line,
            'message': message,
            'severity': severity,
            'timestamp': datetime.now().isoformat()
        })
        self.stats['issues_found'] += 1

    def review_directory(self, directory: str, recursive: bool = True) -> None:
        """Review all files in a directory"""
        exclude_patterns = self.config.get('exclude_patterns', [])

        if recursive:
            for root, dirs, files in os.walk(directory):
                # Filter out excluded directories
                dirs[:] = [d for d in dirs if d not in exclude_patterns]

                for file in files:
                    if not any(file.endswith(pattern) for pattern in exclude_patterns):
                        file_path = os.path.join(root, file)
                        if self._should_review_file(file_path):
                            self.review_file(file_path)
        else:
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path) and self._should_review_file(file_path) and not any(file.endswith(pattern) for pattern in exclude_patterns):
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
            return generate_json_report(self.stats, self.findings)
        elif output_format == 'html':
            return generate_html_report(self.stats, self.findings)
        else:  # text format
            return generate_text_report(self.stats, self.findings)

    def save_report(self, output_path: str, output_format: str = 'text') -> None:
        """Save the report to a file"""
        report = self.generate_report(output_format)

        with open(output_path, 'w') as f:
            f.write(report)

        print(f"Report saved to: {output_path}")



