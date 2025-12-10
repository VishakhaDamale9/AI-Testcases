import os
import json
import argparse
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

import groq
from dotenv import load_dotenv

from analyze_coverage_gaps import (
    analyze_coverage_xml,
    group_by_function,
    DEFAULT_EXCLUDE_PATTERNS,
)

# Load environment variables from .env file
load_dotenv()

# Configuration
API_DIR = Path('backend/app/api')
MODELS_FILE = Path('backend/app/models.py')
CRUD_FILE = Path('backend/app/crud.py')
FEATURE_DIR = Path('backend/app/tests/features')
STEPS_DIR = Path('backend/app/tests/features/steps')
TEMPLATES_FILE = Path('prompt_templates.json')
COVERAGE_XML_PATH = Path('backend/coverage.xml')

# Ensure directories exist
FEATURE_DIR.mkdir(exist_ok=True, parents=True)
STEPS_DIR.mkdir(exist_ok=True, parents=True)

def load_templates() -> Dict[str, Dict[str, str]]:
    """Load prompt templates from JSON file"""
    if not TEMPLATES_FILE.exists():
        raise FileNotFoundError(f"Templates file not found: {TEMPLATES_FILE}")
    
    with open(TEMPLATES_FILE, 'r') as f:
        return json.load(f)

def extract_code_from_response(response_text: str) -> str:
    """Extract clean code from Groq API response."""
    import re
    
    # Remove any markdown code block markers
    # Pattern matches: ```python, ```gherkin, ```, etc.
    cleaned = re.sub(r'^```[a-z]*\n', '', response_text, flags=re.MULTILINE)
    cleaned = re.sub(r'\n```$', '', cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r'^```[a-z]*$', '', cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r'^```$', '', cleaned, flags=re.MULTILINE)
    
    # Remove any remaining ``` markers
    cleaned = cleaned.replace('```', '')
    
    return cleaned.strip()

def call_groq_api(
    prompt_type: str,
    content: str,
    model: str = "llama-3.1-8b-instant",
    coverage_context: str = "",
) -> str:
    """Call Groq API with the specified prompt template and content"""
    if "GROQ_API_KEY" not in os.environ:
        raise ValueError("GROQ_API_KEY environment variable is not set. Please set it to run this script.")

    templates = load_templates()
    
    if prompt_type not in templates:
        raise ValueError(f"Unknown prompt type: {prompt_type}")
    
    template = templates[prompt_type]
    # Build a context dictionary with sensible defaults so `.format` never fails
    default_context = {
        "code": content,
        "feature_content": content,
        "coverage_report": content,
        "function_code": content,
        "model_code": content,
        "coverage_context": coverage_context
        or "No uncovered lines reported; include happy-path, negative, and edge cases.",
    }
    user_prompt = template["user"].format(**default_context)
    
    try:
        client = groq.Groq(api_key=os.environ["GROQ_API_KEY"])
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": template["system"]},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,  # Lower temperature for more deterministic outputs
            max_tokens=2000
        )
        raw_response = response.choices[0].message.content
        # Extract clean code from response
        clean_code = extract_code_from_response(raw_response)
        return clean_code
    except groq.RateLimitError as e:
        print(f"\n  Groq API Rate Limit Reached!")
        print(f"Error: {e}")
        print(f"Please wait ~23 minutes or upgrade your Groq plan.")
        raise e
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        raise e

def extract_api_endpoints():
    """Extract all backend Python files for test generation.
    
    Scans:
    - API routes (backend/app/api/)
    - CRUD operations (backend/app/crud.py)
    - Models (backend/app/models.py)
    - Main app (backend/app/main.py)
    - Utilities (backend/app/utils.py)
    - Core modules (backend/app/core/)
    """
    endpoints = []
    
    # 1. Scan API routes directory
    if API_DIR.exists():
        for root, _, files in os.walk(API_DIR):
            for file in files:
                if file.endswith('.py') and not file.startswith('__'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        content = f.read()
                        endpoints.append({'file': file_path, 'content': content})
    
    # 2. Scan individual core files
    core_files = [
        MODELS_FILE,
        CRUD_FILE,
        Path('backend/app/main.py'),
        Path('backend/app/utils.py'),
    ]
    for file_path in core_files:
        if file_path.exists():
            with open(file_path, 'r') as f:
                content = f.read()
                endpoints.append({'file': str(file_path), 'content': content})
    
    # 3. Scan core/ directory
    core_dir = Path('backend/app/core')
    if core_dir.exists():
        for file in core_dir.glob('*.py'):
            if not file.name.startswith('__'):
                with open(file, 'r') as f:
                    content = f.read()
                    endpoints.append({'file': str(file), 'content': content})
    
    print(f"Found {len(endpoints)} backend files to analyze")
    return endpoints


def _normalize_path_for_lookup(file_path: str) -> str:
    """Normalize file paths for coverage lookup comparisons."""
    return Path(file_path).as_posix().replace("backend/app/", "").lstrip("./")


def _build_coverage_lookup(coverage_xml: Path) -> Dict[str, str]:
    """Create a lookup of coverage gaps per file (normalized path -> text)."""
    if not coverage_xml.exists():
        print(f"Coverage XML not found at {coverage_xml}. Continuing without coverage hints.")
        return {}

    coverage_data = analyze_coverage_xml(str(coverage_xml), DEFAULT_EXCLUDE_PATTERNS)
    if not coverage_data:
        print("Coverage data could not be parsed. Continuing without coverage hints.")
        return {}

    lookup: Dict[str, str] = {}
    for filename, uncovered_lines in coverage_data["uncovered_by_file"].items():
        normalized = _normalize_path_for_lookup(filename)
        if not uncovered_lines:
            lookup[normalized] = "No uncovered lines; aim for auth, validation, and edge cases."
            continue

        grouped = group_by_function(uncovered_lines)
        parts: List[str] = []
        for function_name, lines in sorted(grouped.items()):
            func_label = function_name or "unknown"
            line_list = ", ".join(map(str, sorted(lines)))
            parts.append(f"- {func_label}: lines {line_list}")

        lookup[normalized] = "\n".join(parts)

    print(f"Loaded coverage hints for {len(lookup)} files from {coverage_xml}")
    return lookup

def generate_feature_file(
    endpoint_info: Dict[str, str],
    coverage_context: str,
    model: str,
    output_path: Optional[Path] = None,
) -> Tuple[Path, str]:
    """Generate a Gherkin feature file for an API endpoint"""
    print(f"Generating feature file for: {endpoint_info['file']}")
    
    # Call Groq API to generate feature content
    feature_content = call_groq_api(
        "endpoint_analysis",
        endpoint_info['content'],
        model=model,
        coverage_context=coverage_context,
    )
    
    # Write feature file if output path is provided
    if output_path:
        with open(output_path, 'w') as f:
            f.write(feature_content)
        print(f"Generated feature file: {output_path}")
    else:
        # Generate output path based on file name
        file_name = os.path.basename(endpoint_info['file']).replace('.py', '')
        output_path = FEATURE_DIR / f"{file_name}.feature"
        with open(output_path, 'w') as f:
            f.write(feature_content)
        print(f"Generated feature file: {output_path}")
    
    return output_path, feature_content

def generate_step_definitions(
    feature_path: Path,
    feature_content: str,
    model: str,
) -> Path:
    """Generate step definitions for a feature file"""
    feature_name = os.path.basename(feature_path).replace('.feature', '')
    print(f"Generating step definitions for: {feature_name}")
    
    # Call Groq API to generate step definitions
    step_content = call_groq_api("step_definition", feature_content, model=model)
    
    # Write step file
    step_file = STEPS_DIR / f"{feature_name}_steps.py"
    with open(step_file, 'w') as f:
        f.write(step_content)
    
    print(f"Generated step definition file: {step_file}")
    return step_file

def main():
    parser = argparse.ArgumentParser(description='Generate BDD tests using Groq API')
    parser.add_argument('--api-key', type=str, help='Groq API key')
    parser.add_argument('--model', type=str, default='llama-3.1-8b-instant', help='Groq model to use')
    parser.add_argument('--endpoint', type=str, help='Specific API endpoint file to analyze')
    parser.add_argument('--coverage-xml', type=str, default=str(COVERAGE_XML_PATH),
                        help='Coverage XML file to prioritize uncovered lines')
    args = parser.parse_args()
    
    # Set Groq API key if provided
    if args.api_key:
        os.environ["GROQ_API_KEY"] = args.api_key
    # Otherwise use the one from .env file (already loaded into environment)
    
    print("Starting BDD test generation with Groq...")
    
    # Extract API endpoints
    if args.endpoint and os.path.exists(args.endpoint):
        print(f"Analyzing specific endpoint: {args.endpoint}")
        with open(args.endpoint, 'r') as f:
            content = f.read()
        endpoints = [{'file': args.endpoint, 'content': content}]
    else:
        print("Extracting API endpoints...")
        endpoints = extract_api_endpoints()
    
    print(f"Found {len(endpoints)} API endpoint files")

    # Load coverage hints if available
    coverage_lookup = _build_coverage_lookup(Path(args.coverage_xml))
    
    # Generate feature files and step definitions
    for endpoint in endpoints:
        normalized_path = _normalize_path_for_lookup(endpoint["file"])
        coverage_context = coverage_lookup.get(
            normalized_path,
            "No uncovered lines reported; include auth failures, validation errors, and edge cases.",
        )

        # Generate feature file
        feature_path, feature_content = generate_feature_file(
            endpoint,
            coverage_context=coverage_context,
            model=args.model,
        )
        
        # Generate step definitions
        generate_step_definitions(feature_path, feature_content, model=args.model)
        
        # Delay to avoid rate limiting
        time.sleep(1)
    
    print("\nBDD test generation complete!")
    print("Run the tests with: cd backend && python -m behave app/tests/features")

if __name__ == "__main__":
    main()