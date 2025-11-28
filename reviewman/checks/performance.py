import re
from typing import List

def check_performance_issues(file_path: str, content: str, lines: List[str], config: dict) -> List[dict]:
    """Check for performance issues"""
    findings = []
    for i, line in enumerate(lines, 1):
        # Check for inefficient loops
        if re.search(r'for\s+\w+\s+in\s+range\s*\(\s*len\s*\(', line):
            findings.append({
                'category': 'performance',
                'file_path': file_path,
                'line': i,
                'message': "Using range(len()) - consider enumerate() or direct iteration",
                'severity': 'low'
            })

        # Check for string concatenation in loops
        if '+=' in line and 'str' in line.lower():
            findings.append({
                'category': 'performance',
                'file_path': file_path,
                'line': i,
                'message': "String concatenation with += can be slow - consider join()",
                'severity': 'medium'
            })

        # Check for global variables
        if re.match(r'^[A-Z_]+\s*=\s*', line) and not line.strip().startswith('#'):
            findings.append({
                'category': 'performance',
                'file_path': file_path,
                'line': i,
                'message': "Global variable detected - can impact performance and testing",
                'severity': 'low'
            })

        # Check for multiple API calls in loop
        if 'for ' in line or 'while ' in line:
            next_lines = lines[i:min(i+10, len(lines))]
            if any('requests.' in l or 'http' in l.lower() for l in next_lines):
                findings.append({
                    'category': 'performance',
                    'file_path': file_path,
                    'line': i,
                    'message': "Potential API calls in loop - consider batch operations",
                    'severity': 'high'
                })
    return findings
