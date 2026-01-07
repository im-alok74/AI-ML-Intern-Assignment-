"""
TalentScout - Logic Demonstration
This script demonstrates the core conversation flow logic without requiring API keys.
Useful for understanding the step-by-step screening process.
"""

from prompts import CANDIDATE_INFO_FIELDS, GREETING_MESSAGE, EXIT_MESSAGE
from utils import (
    parse_tech_stack,
    validate_email,
    validate_phone,
    validate_experience,
    is_exit_command
)


def demo_conversation_flow():
    """Demonstrate the conversation flow logic."""
    print("=" * 70)
    print("TalentScout Hiring Assistant - Logic Flow Demo")
    print("=" * 70)
    print("\nThis demo shows how the chatbot processes information step-by-step.\n")

    print("\n1. GREETING STAGE")
    print("-" * 70)
    print(f"Chatbot: {GREETING_MESSAGE}")

    print("\n2. INFORMATION COLLECTION STAGE (7 steps)")
    print("-" * 70)

    for idx, field_info in enumerate(CANDIDATE_INFO_FIELDS, 1):
        field_name = field_info['field']
        prompt = field_info['prompt']

        print(f"\nStep {idx}: Collecting '{field_name}'")
        print(f"Chatbot: {prompt}")

        if field_name == 'email':
            print("Example valid input: 'john.doe@example.com'")
            print(f"  Validation result: {validate_email('john.doe@example.com')}")
            print("Example invalid input: 'not-an-email'")
            print(f"  Validation result: {validate_email('not-an-email')}")

        elif field_name == 'phone':
            print("Example valid input: '+1-555-123-4567'")
            print(f"  Validation result: {validate_phone('+1-555-123-4567')}")
            print("Example invalid input: '123'")
            print(f"  Validation result: {validate_phone('123')}")

        elif field_name == 'experience':
            print("Example valid input: '5 years'")
            print(f"  Validation result: {validate_experience('5 years')}")
            print("Example invalid input: 'lots'")
            print(f"  Validation result: {validate_experience('lots')}")

        elif field_name == 'tech_stack':
            print("Example input: 'Python, Django, PostgreSQL'")
            result = parse_tech_stack('Python, Django, PostgreSQL')
            print(f"  Parsed result: {result}")
            print("\nExample input: 'Python Django PostgreSQL'")
            result = parse_tech_stack('Python Django PostgreSQL')
            print(f"  Parsed result: {result}")

    print("\n3. TECHNICAL QUESTION GENERATION STAGE")
    print("-" * 70)
    print("After collecting tech stack, the chatbot uses Google Gemini to generate:")
    print("  - 3-5 questions per technology")
    print("  - Mix of conceptual, implementation, and scenario-based questions")
    print("  - No answers included (interview-ready format)")

    print("\n4. EXIT HANDLING")
    print("-" * 70)
    print("Exit keywords: exit, quit, bye, thank you")
    print(f"\nTest 'exit': {is_exit_command('exit')}")
    print(f"Test 'thank you': {is_exit_command('thank you')}")
    print(f"Test 'hello': {is_exit_command('hello')}")
    print(f"\nExit message: {EXIT_MESSAGE}")

    print("\n5. KEY FEATURES SUMMARY")
    print("-" * 70)
    print("✓ Sequential information collection (no skipping)")
    print("✓ Input validation at each step")
    print("✓ Flexible tech stack input format")
    print("✓ AI-powered question generation")
    print("✓ Context-aware conversation flow")
    print("✓ Professional exit handling")
    print("✓ In-memory storage only (GDPR compliant)")

    print("\n" + "=" * 70)
    print("End of Logic Flow Demo")
    print("=" * 70)
    print("\nTo see this in action, run: streamlit run app.py")


if __name__ == "__main__":
    demo_conversation_flow()
