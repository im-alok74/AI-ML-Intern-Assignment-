"""
Quick test script to verify all imports and basic functionality.
"""

def test_imports():
    """Test that all modules can be imported successfully."""
    print("Testing imports...")

    try:
        import prompts
        print("✓ prompts.py imported successfully")
    except Exception as e:
        print(f"✗ Error importing prompts: {e}")
        return False

    try:
        import utils
        print("✓ utils.py imported successfully")
    except Exception as e:
        print(f"✗ Error importing utils: {e}")
        return False

    try:
        import chatbot
        print("✓ chatbot.py imported successfully")
    except Exception as e:
        print(f"✗ Error importing chatbot: {e}")
        return False

    return True


def test_utils():
    """Test utility functions."""
    print("\nTesting utility functions...")

    from utils import parse_tech_stack, validate_email, validate_phone, is_exit_command

    tech1 = parse_tech_stack("Python, Django, SQL")
    assert tech1 == ['Python', 'Django', 'SQL'], f"Tech stack parsing failed: {tech1}"
    print("✓ Tech stack parsing (comma-separated) works")

    tech2 = parse_tech_stack("Python Django SQL")
    assert tech2 == ['Python', 'Django', 'SQL'], f"Tech stack parsing failed: {tech2}"
    print("✓ Tech stack parsing (space-separated) works")

    assert validate_email("test@example.com") == True
    assert validate_email("invalid-email") == False
    print("✓ Email validation works")

    assert validate_phone("555-123-4567") == True
    assert validate_phone("123") == False
    print("✓ Phone validation works")

    assert is_exit_command("exit") == True
    assert is_exit_command("thank you") == True
    assert is_exit_command("hello") == False
    print("✓ Exit command detection works")


def test_prompts():
    """Test prompt templates exist."""
    print("\nTesting prompt templates...")

    from prompts import (
        SYSTEM_PROMPT,
        GREETING_MESSAGE,
        EXIT_MESSAGE,
        CANDIDATE_INFO_FIELDS
    )

    assert len(SYSTEM_PROMPT) > 0
    print("✓ System prompt exists")

    assert len(GREETING_MESSAGE) > 0
    print("✓ Greeting message exists")

    assert len(EXIT_MESSAGE) > 0
    print("✓ Exit message exists")

    assert len(CANDIDATE_INFO_FIELDS) == 7
    print("✓ All 7 candidate info fields defined")


if __name__ == "__main__":
    print("=" * 60)
    print("TalentScout Hiring Assistant - Test Suite")
    print("=" * 60)

    if not test_imports():
        print("\n✗ Import tests failed!")
        exit(1)

    try:
        test_utils()
        test_prompts()

        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        print("\nThe application is ready to run with: streamlit run app.py")

    except Exception as e:
        print(f"\n✗ Tests failed: {e}")
        exit(1)
