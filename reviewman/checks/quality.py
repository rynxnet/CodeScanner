import re
from typing import List

def check_code_quality(file_path: str, lines: List[str], config: dict) -> List[dict]:
    """Check code quality issues"""
    findings = []
    for i, line in enumerate(lines, 1):
        # Check line length
        if len(line) > config.get('max_line_length', 100):
            findings.append({
                'category': 'quality',
                'file_path': file_path,
                'line': i,
                'message': f"Line exceeds {config.get('max_line_length', 100)} characters ({len(line)})",
                'severity': 'low'
            })

        # Check for TODO/FIXME comments
        if 'TODO' in line or 'FIXME' in line:
            findings.append({
                'category': 'quality',
                'file_path': file_path,
                'line': i,
                'message': "TODO/FIXME comment found - should be addressed",
                'severity': 'info'
            })

        # Check for trailing whitespace
        if line.endswith(' ') or line.endswith('\t'):
            findings.append({
                'category': 'quality',
                'file_path': file_path,
                'line': i,
                'message': "Trailing whitespace detected",
                'severity': 'low'
            })

        # Check for print statements (potential debug code)
        if re.search(r'^\s*print\s*\(', line) and not line.strip().startswith('#'):
            findings.append({
                'category': 'quality',
                'file_path': file_path,
                'line': i,
                'message': "Print statement detected - use logging instead",
                'severity': 'medium'
            })

        # Check for commented-out code
        stripped = line.strip()
        if stripped.startswith('#') and len(stripped) > 2:
            code_patterns = ['def ', 'class ', 'import ', 'if ', 'for ', 'while ']
            if any(pattern in stripped[1:] for pattern in code_patterns):
                findings.append({
                    'category': 'quality',
                    'file_path': file_path,
                    'line': i,
                    'message': "Commented-out code detected - should be removed",
                    'severity': 'low'
                })
    return findings
