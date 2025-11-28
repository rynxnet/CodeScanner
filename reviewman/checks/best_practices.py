from typing import List

def check_best_practices(file_path: str, content: str, lines: List[str], config: dict) -> List[dict]:
    """Check for best practice violations"""
    findings = []
    # Check for proper docstrings
    if file_path.endswith('.py'):
        if 'def ' in content and '"""' not in content:
            findings.append({
                'category': 'best_practices',
                'file_path': file_path,
                'line': 0,
                'message': "Functions found without docstrings",
                'severity': 'medium'
            })

        # Check for proper imports
        import_section = '\n'.join(lines[:50])  # Check first 50 lines
        if 'import *' in import_section:
            findings.append({
                'category': 'best_practices',
                'file_path': file_path,
                'line': 0,
                'message': "Wildcard imports (import *) discouraged",
                'severity': 'medium'
            })

    # Check for exception handling
    try_blocks = content.count('try:')
    bare_excepts = content.count('except:')
    if bare_excepts > 0:
        findings.append({
            'category': 'best_practices',
            'file_path': file_path,
            'line': 0,
            'message': "Bare except clause found - specify exception types",
            'severity': 'medium'
        })

    # Check file size
    if len(lines) > 500:
        findings.append({
            'category': 'best_practices',
            'file_path': file_path,
            'line': 0,
            'message': f"Large file ({len(lines)} lines) - consider splitting",
            'severity': 'low'
        })
    return findings
