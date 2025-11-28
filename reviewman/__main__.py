import argparse
import os
import sys
from .reviewman import CodeReviewer

def main():
    parser = argparse.ArgumentParser(
        description='ReviewMan - Comprehensive Code Review Assistant',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m reviewman file.py              # Review a single file
  python -m reviewman ./src --recursive    # Review directory recursively
  python -m reviewman ./src -f html -o report.html  # Generate HTML report
  python -m reviewman ./src --config config.json # Use custom configuration
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
