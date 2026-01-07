"""
TalentScout Hiring Assistant - Utility Functions
This module contains helper functions for input validation and parsing.
"""

import re
from typing import List


def parse_tech_stack(tech_stack_input: str) -> List[str]:
    """
    Parse tech stack input and normalize it into a clean list.
    Handles both comma-separated and space-separated inputs.

    Args:
        tech_stack_input: Raw tech stack string from user

    Returns:
        List of cleaned technology names

    Examples:
        >>> parse_tech_stack("Python, Django, SQL")
        ['Python', 'Django', 'SQL']
        >>> parse_tech_stack("Python Django SQL")
        ['Python', 'Django', 'SQL']
    """
    if not tech_stack_input:
        return []

    tech_stack_input = tech_stack_input.strip()

    if ',' in tech_stack_input:
        technologies = [tech.strip() for tech in tech_stack_input.split(',')]
    else:
        technologies = [tech.strip() for tech in tech_stack_input.split()]

    technologies = [tech for tech in technologies if tech]

    return technologies


def validate_email(email: str) -> bool:
    """
    Validate email format using regex pattern.

    Args:
        email: Email address to validate

    Returns:
        True if email format is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format.
    Accepts various formats with optional country codes, spaces, dashes, and parentheses.

    Args:
        phone: Phone number to validate

    Returns:
        True if phone format is valid, False otherwise
    """
    cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
    return len(cleaned) >= 10 and cleaned.isdigit()


def validate_experience(experience: str) -> bool:
    """
    Validate years of experience input.
    Accepts numeric values and common formats like "5 years", "2.5", etc.

    Args:
        experience: Experience string to validate

    Returns:
        True if experience format is valid, False otherwise
    """
    cleaned = experience.strip().lower()
    cleaned = re.sub(r'\s*(years?|yrs?)\s*', '', cleaned)

    try:
        exp_value = float(cleaned)
        return 0 <= exp_value <= 50
    except ValueError:
        return False


def is_exit_command(user_input: str) -> bool:
    """
    Check if user input indicates intent to exit the conversation.

    Args:
        user_input: User's message

    Returns:
        True if input contains exit keywords, False otherwise
    """
    exit_keywords = ['exit', 'quit', 'bye', 'thank you', 'thanks']
    user_input_lower = user_input.lower().strip()

    return any(keyword in user_input_lower for keyword in exit_keywords)


def format_candidate_summary(candidate_data: dict) -> str:
    """
    Format candidate data into a readable summary.

    Args:
        candidate_data: Dictionary containing candidate information

    Returns:
        Formatted string summary of candidate data
    """
    summary = "**Candidate Summary**\n\n"

    field_labels = {
        'full_name': 'Full Name',
        'email': 'Email',
        'phone': 'Phone',
        'experience': 'Years of Experience',
        'position': 'Desired Position(s)',
        'location': 'Current Location',
        'tech_stack': 'Tech Stack'
    }

    for field, label in field_labels.items():
        if field in candidate_data and candidate_data[field]:
            value = candidate_data[field]
            if field == 'tech_stack' and isinstance(value, list):
                value = ', '.join(value)
            summary += f"**{label}:** {value}\n"

    return summary


def sanitize_input(user_input: str) -> str:
    """
    Sanitize user input to prevent injection or malicious content.

    Args:
        user_input: Raw user input

    Returns:
        Sanitized string
    """
    if not user_input:
        return ""

    sanitized = user_input.strip()

    sanitized = re.sub(r'[<>]', '', sanitized)

    return sanitized[:500]
