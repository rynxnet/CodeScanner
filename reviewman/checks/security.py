import re
from typing import List

def check_security_issues(file_path: str, content: str, lines: List[str], config: dict) -> List[dict]:
    """Check for security vulnerabilities"""
    findings = []
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
                findings.append({
                    'category': 'security',
                    'file_path': file_path,
                    'line': i,
                    'message': message,
                    'severity': severity
                })

    # Check for missing input validation
    if 'input(' in content and 'validate' not in content.lower():
        findings.append({
            'category': 'security',
            'file_path': file_path,
            'line': 0,
            'message': "User input detected without apparent validation",
            'severity': 'medium'
        })
    return findings
