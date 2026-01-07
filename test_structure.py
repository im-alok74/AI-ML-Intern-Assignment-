"""
Structure and syntax validation test.
Tests the codebase structure without requiring external dependencies.
"""

import ast
import os


def test_file_exists(filepath):
    """Check if a file exists."""
    if os.path.exists(filepath):
        print(f"✓ {filepath} exists")
        return True
    else:
        print(f"✗ {filepath} missing")
        return False


def test_python_syntax(filepath):
    """Check if a Python file has valid syntax."""
    try:
        with open(filepath, 'r') as f:
            ast.parse(f.read())
        print(f"✓ {filepath} has valid Python syntax")
        return True
    except SyntaxError as e:
        print(f"✗ {filepath} has syntax error: {e}")
        return False


def test_required_functions(filepath, required_items):
    """Check if required functions/classes exist in a module."""
    try:
        with open(filepath, 'r') as f:
            tree = ast.parse(f.read())

        defined_items = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                defined_items.add(node.name)
            elif isinstance(node, ast.ClassDef):
                defined_items.add(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        defined_items.add(target.id)

        missing = set(required_items) - defined_items
        if not missing:
            print(f"✓ {filepath} contains all required items")
            return True
        else:
            print(f"✗ {filepath} missing: {missing}")
            return False

    except Exception as e:
        print(f"✗ Error checking {filepath}: {e}")
        return False


def main():
    print("=" * 70)
    print("TalentScout Hiring Assistant - Structure Validation")
    print("=" * 70)

    all_tests_passed = True

    print("\n1. Checking Required Files...")
    required_files = [
        'app.py',
        'chatbot.py',
        'prompts.py',
        'utils.py',
        'requirements.txt',
        '.env.example',
        'README.md',
        '.gitignore'
    ]

    for file in required_files:
        if not test_file_exists(file):
            all_tests_passed = False

    print("\n2. Validating Python Syntax...")
    python_files = ['app.py', 'chatbot.py', 'prompts.py', 'utils.py']

    for file in python_files:
        if not test_python_syntax(file):
            all_tests_passed = False

    print("\n3. Checking Module Structure...")

    utils_required = [
        'parse_tech_stack',
        'validate_email',
        'validate_phone',
        'validate_experience',
        'is_exit_command'
    ]
    if not test_required_functions('utils.py', utils_required):
        all_tests_passed = False

    prompts_required = [
        'SYSTEM_PROMPT',
        'GREETING_MESSAGE',
        'EXIT_MESSAGE',
        'CANDIDATE_INFO_FIELDS',
        'TECHNICAL_QUESTION_GENERATION_PROMPT'
    ]
    if not test_required_functions('prompts.py', prompts_required):
        all_tests_passed = False

    chatbot_required = ['HiringAssistant']
    if not test_required_functions('chatbot.py', chatbot_required):
        all_tests_passed = False

    app_required = ['initialize_session_state', 'main']
    if not test_required_functions('app.py', app_required):
        all_tests_passed = False

    print("\n4. Checking Requirements File...")
    with open('requirements.txt', 'r') as f:
        requirements = f.read()
        required_packages = ['streamlit', 'google-generativeai', 'python-dotenv']
        for package in required_packages:
            if package in requirements:
                print(f"✓ {package} listed in requirements.txt")
            else:
                print(f"✗ {package} missing from requirements.txt")
                all_tests_passed = False

    print("\n5. Checking README.md Structure...")
    with open('README.md', 'r') as f:
        readme = f.read()
        required_sections = [
            '# TalentScout',
            '## Features',
            '## Installation',
            '## Usage',
            '## Prompt Engineering',
            '## Architecture',
            '## Privacy',
            '## Challenges'
        ]
        for section in required_sections:
            if section in readme:
                print(f"✓ README contains '{section}' section")
            else:
                print(f"✗ README missing '{section}' section")
                all_tests_passed = False

    print("\n" + "=" * 70)
    if all_tests_passed:
        print("✓ ALL STRUCTURE TESTS PASSED!")
        print("=" * 70)
        print("\nNext Steps:")
        print("1. Create a virtual environment: python3 -m venv venv")
        print("2. Activate it: source venv/bin/activate")
        print("3. Install dependencies: pip install -r requirements.txt")
        print("4. Set up .env file with your GEMINI_API_KEY")
        print("5. Run the app: streamlit run app.py")
        return 0
    else:
        print("✗ SOME TESTS FAILED!")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    exit(main())
