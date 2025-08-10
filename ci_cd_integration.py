#!/usr/bin/env python
"""
CI/CD Integration Script for BDD Test Generation

This script demonstrates how to integrate the BDD test generation process
with a CI/CD pipeline. It can be used in GitHub Actions, GitLab CI, Jenkins, etc.

Usage:
    python ci_cd_integration.py [--target-coverage PERCENTAGE] [--max-iterations NUMBER]
"""

import os
import sys
import argparse
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

# Configuration
BACKEND_DIR = Path('backend')
FEATURE_DIR = BACKEND_DIR / 'app' / 'tests' / 'features'
COVERAGE_XML = BACKEND_DIR / 'coverage.xml'
GROQ_GENERATOR = Path('groq_bdd_generator.py')

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='CI/CD Integration for BDD Test Generation')
    parser.add_argument('--target-coverage', type=float, default=100.0,
                        help='Target coverage percentage (default: 100.0)')
    parser.add_argument('--max-iterations', type=int, default=3,
                        help='Maximum number of test generation iterations (default: 3)')
    parser.add_argument('--api-key', type=str, help='Groq API key')
    parser.add_argument('--model', type=str, default='llama3-70b-8192',
                        help='Groq model to use (default: llama3-70b-8192)')
    return parser.parse_args()

def run_command(command, cwd=None):
    """Run a shell command and return the output"""
    print(f"Running command: {command}")
    result = subprocess.run(
        command,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
    
    return result

def get_current_coverage():
    """Run pytest with coverage and return the coverage percentage"""
    # Run pytest with coverage
    result = run_command(
        "python -m pytest --cov=app --cov-report=xml --cov-report=term",
        cwd=BACKEND_DIR
    )
    
    # Parse coverage.xml to get the coverage percentage
    if not COVERAGE_XML.exists():
        print(f"Coverage XML file not found: {COVERAGE_XML}")
        return 0.0
    
    try:
        tree = ET.parse(COVERAGE_XML)
        root = tree.getroot()
        coverage = float(root.attrib.get('line-rate', '0')) * 100
        return coverage
    except Exception as e:
        print(f"Error parsing coverage XML: {e}")
        return 0.0

def run_bdd_tests():
    """Run the BDD tests using behave"""
    if not FEATURE_DIR.exists():
        print(f"Feature directory not found: {FEATURE_DIR}")
        return False
    
    result = run_command(
        "python -m behave app/tests/features",
        cwd=BACKEND_DIR
    )
    
    return result.returncode == 0

def generate_bdd_tests(api_key=None, model='llama3-70b-8192'):
    """Generate BDD tests using the Groq generator"""
    if not GROQ_GENERATOR.exists():
        print(f"Groq generator script not found: {GROQ_GENERATOR}")
        return False
    
    cmd = f"python {GROQ_GENERATOR}"
    if api_key:
        cmd += f" --api-key {api_key}"
    if model:
        cmd += f" --model {model}"
    
    result = run_command(cmd)
    return result.returncode == 0

def main():
    """Main function"""
    args = parse_args()
    
    # Set Groq API key if provided
    if args.api_key:
        os.environ["GROQ_API_KEY"] = args.api_key
    # Otherwise use the one from .env file (already loaded into environment)
    
    print("=== CI/CD Integration for BDD Test Generation ===")
    print(f"Target coverage: {args.target_coverage}%")
    print(f"Maximum iterations: {args.max_iterations}")
    
    # Get initial coverage
    print("\n=== Initial Coverage Analysis ===")
    initial_coverage = get_current_coverage()
    print(f"Initial coverage: {initial_coverage:.2f}%")
    
    # Check if we already meet the target coverage
    if initial_coverage >= args.target_coverage:
        print(f"Initial coverage ({initial_coverage:.2f}%) already meets target ({args.target_coverage}%)")
        return 0
    
    # Generate and run BDD tests
    iteration = 1
    current_coverage = initial_coverage
    previous_coverage = 0.0
    
    while (current_coverage < args.target_coverage and 
           iteration <= args.max_iterations and 
           current_coverage > previous_coverage):
        print(f"\n=== Iteration {iteration} ===")
        
        # Generate BDD tests
        print("Generating BDD tests...")
        if not generate_bdd_tests(args.api_key, args.model):
            print("Failed to generate BDD tests")
            return 1
        
        # Run BDD tests
        print("Running BDD tests...")
        if not run_bdd_tests():
            print("BDD tests failed")
            return 1
        
        # Get new coverage
        previous_coverage = current_coverage
        current_coverage = get_current_coverage()
        print(f"Current coverage: {current_coverage:.2f}%")
        
        iteration += 1
    
    # Final coverage check
    print("\n=== Final Coverage Analysis ===")
    final_coverage = get_current_coverage()
    print(f"Final coverage: {final_coverage:.2f}%")
    print(f"Coverage improvement: {final_coverage - initial_coverage:.2f}%")
    
    # Check if we met the target coverage
    if final_coverage >= args.target_coverage:
        print(f"Success! Target coverage ({args.target_coverage}%) achieved.")
        return 0
    else:
        print(f"Warning: Target coverage ({args.target_coverage}%) not achieved.")
        print(f"Current coverage: {final_coverage:.2f}%")
        return 1

if __name__ == "__main__":
    sys.exit(main())