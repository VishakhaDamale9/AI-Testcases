#!/usr/bin/env python
"""
Coverage Gap Analysis Script

This script analyzes the current test coverage and identifies gaps that need to be addressed
to achieve 100% coverage. It parses the coverage XML report and outputs a list of uncovered
lines and functions, grouped by file.

Usage:
    python analyze_coverage_gaps.py [--coverage-xml PATH] [--exclude-patterns PATTERNS]
"""

import os
import sys
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
import re
from collections import defaultdict

# Default configuration
DEFAULT_COVERAGE_XML = Path('backend/coverage.xml')
DEFAULT_EXCLUDE_PATTERNS = [
    r'__pycache__',
    r'/migrations/',
    r'/alembic/',
    r'/tests/',
    r'__init__.py'
]

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Analyze test coverage gaps')
    parser.add_argument('--coverage-xml', type=str, default=str(DEFAULT_COVERAGE_XML),
                        help=f'Path to coverage XML report (default: {DEFAULT_COVERAGE_XML})')
    parser.add_argument('--exclude-patterns', type=str, nargs='+', default=DEFAULT_EXCLUDE_PATTERNS,
                        help='Patterns to exclude from analysis')
    return parser.parse_args()

def should_exclude(path, exclude_patterns):
    """Check if a path should be excluded based on patterns"""
    for pattern in exclude_patterns:
        if re.search(pattern, path):
            return True
    return False

def extract_function_name(line, file_content):
    """Extract function name from a line number"""
    if not file_content:
        return None
    
    lines = file_content.split('\n')
    if line > len(lines):
        return None
    
    # Look for function definition in current line and above
    for i in range(line, max(0, line-10), -1):
        if i-1 >= len(lines):
            continue
        current_line = lines[i-1].strip()
        # Match function or method definition
        match = re.match(r'^(async\s+)?def\s+([a-zA-Z0-9_]+)\s*\(', current_line)
        if match:
            return match.group(2)
        # Match class definition
        match = re.match(r'^class\s+([a-zA-Z0-9_]+)\s*[\(:]', current_line)
        if match:
            return match.group(1)
    
    return None

def read_file_content(file_path):
    """Read file content safely"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def analyze_coverage_xml(coverage_xml_path, exclude_patterns):
    """Analyze coverage XML report and identify gaps"""
    if not os.path.exists(coverage_xml_path):
        print(f"Coverage XML file not found: {coverage_xml_path}")
        return None
    
    try:
        tree = ET.parse(coverage_xml_path)
        root = tree.getroot()
        
        # Extract overall coverage
        overall_coverage = float(root.attrib.get('line-rate', '0')) * 100
        
        # Extract uncovered lines by file
        uncovered_by_file = defaultdict(list)
        
        for package in root.findall('.//package'):
            for class_elem in package.findall('.//class'):
                filename = class_elem.attrib.get('filename')
                
                # Skip excluded files
                if should_exclude(filename, exclude_patterns):
                    continue
                
                # Get file content for function name extraction
                file_path = os.path.join(os.path.dirname(coverage_xml_path), '..', filename)
                file_content = read_file_content(file_path)
                
                for line in class_elem.findall('.//line'):
                    hits = int(line.attrib.get('hits', '0'))
                    if hits == 0:  # Uncovered line
                        line_number = int(line.attrib.get('number', '0'))
                        function_name = extract_function_name(line_number, file_content)
                        uncovered_by_file[filename].append({
                            'line': line_number,
                            'function': function_name
                        })
        
        return {
            'overall_coverage': overall_coverage,
            'uncovered_by_file': uncovered_by_file
        }
    
    except Exception as e:
        print(f"Error parsing coverage XML: {e}")
        return None

def group_by_function(uncovered_lines):
    """Group uncovered lines by function"""
    by_function = defaultdict(list)
    
    for line_info in uncovered_lines:
        function = line_info['function'] or 'unknown'
        by_function[function].append(line_info['line'])
    
    return by_function

def print_coverage_gaps(coverage_data):
    """Print coverage gaps in a readable format"""
    if not coverage_data:
        print("No coverage data available.")
        return
    
    overall_coverage = coverage_data['overall_coverage']
    uncovered_by_file = coverage_data['uncovered_by_file']
    
    print(f"\n=== Coverage Gap Analysis ===\n")
    print(f"Overall coverage: {overall_coverage:.2f}%")
    print(f"Coverage gap: {100 - overall_coverage:.2f}%")
    print(f"\nUncovered code by file:\n")
    
    for filename, uncovered_lines in sorted(uncovered_by_file.items()):
        if not uncovered_lines:
            continue
        
        print(f"File: {filename}")
        by_function = group_by_function(uncovered_lines)
        
        for function, lines in sorted(by_function.items()):
            print(f"  Function: {function}")
            print(f"    Lines: {', '.join(map(str, sorted(lines)))}")
        
        print()

def generate_bdd_suggestions(coverage_data):
    """Generate BDD test suggestions for uncovered code"""
    if not coverage_data:
        return
    
    print("\n=== BDD Test Suggestions ===\n")
    
    for filename, uncovered_lines in sorted(coverage_data['uncovered_by_file'].items()):
        if not uncovered_lines:
            continue
        
        print(f"File: {filename}")
        by_function = group_by_function(uncovered_lines)
        
        for function, lines in sorted(by_function.items()):
            if function == 'unknown':
                continue
            
            print(f"  Function: {function}")
            print(f"  Suggested BDD Scenarios:")
            
            # Generate basic scenarios based on function name
            if 'create' in function.lower() or 'add' in function.lower():
                print("    Scenario: Create with valid data")
                print("    Scenario: Create with invalid data")
                print("    Scenario: Create with missing required fields")
            
            elif 'update' in function.lower() or 'edit' in function.lower():
                print("    Scenario: Update with valid data")
                print("    Scenario: Update with invalid data")
                print("    Scenario: Update non-existent resource")
            
            elif 'delete' in function.lower() or 'remove' in function.lower():
                print("    Scenario: Delete existing resource")
                print("    Scenario: Delete non-existent resource")
                print("    Scenario: Delete with insufficient permissions")
            
            elif 'get' in function.lower() or 'read' in function.lower() or 'list' in function.lower():
                print("    Scenario: Get existing resource")
                print("    Scenario: Get non-existent resource")
                print("    Scenario: List with pagination")
                print("    Scenario: List with filtering")
            
            elif 'validate' in function.lower() or 'verify' in function.lower():
                print("    Scenario: Validate with valid data")
                print("    Scenario: Validate with invalid data")
                print("    Scenario: Validate with edge cases")
            
            elif 'auth' in function.lower() or 'login' in function.lower() or 'permission' in function.lower():
                print("    Scenario: Authenticate with valid credentials")
                print("    Scenario: Authenticate with invalid credentials")
                print("    Scenario: Access with insufficient permissions")
                print("    Scenario: Access with expired token")
            
            else:
                print("    Scenario: Execute function with valid parameters")
                print("    Scenario: Execute function with invalid parameters")
                print("    Scenario: Execute function with edge case values")
            
            print()

def main():
    """Main function"""
    args = parse_args()
    
    # Analyze coverage XML
    coverage_data = analyze_coverage_xml(args.coverage_xml, args.exclude_patterns)
    
    if not coverage_data:
        print("Failed to analyze coverage data.")
        return 1
    
    # Print coverage gaps
    print_coverage_gaps(coverage_data)
    
    # Generate BDD suggestions
    generate_bdd_suggestions(coverage_data)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())