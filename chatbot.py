"""
TalentScout Hiring Assistant - Chatbot Controller
This module manages conversation flow, state, and LLM interactions.

NOTE: All data is stored in-memory only (Streamlit session_state).
No persistent storage is used to ensure GDPR compliance and data privacy.
"""

import os
from typing import Dict, Optional, Tuple
import google.generativeai as genai

from prompts import (
    SYSTEM_PROMPT,
    INFORMATION_COLLECTION_PROMPT,
    TECHNICAL_QUESTION_GENERATION_PROMPT,
    GREETING_MESSAGE,
    EXIT_MESSAGE,
    CANDIDATE_INFO_FIELDS
)
from utils import (
    parse_tech_stack,
    validate_email,
    validate_phone,
    validate_experience,
    is_exit_command,
    sanitize_input
)


class HiringAssistant:
    """
    Main chatbot controller for TalentScout Hiring Assistant.
    Manages conversation state, candidate data collection, and technical question generation.
    """

    def __init__(self, api_key: str):
        """
        Initialize the Hiring Assistant chatbot.

        Args:
            api_key: Google Gemini API key
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

        self.current_field_index = 0
        self.candidate_data = {}
        self.conversation_active = True
        self.tech_questions_generated = False

    def get_greeting(self) -> str:
        """
        Get the initial greeting message.

        Returns:
            Greeting message string
        """
        return GREETING_MESSAGE

    def should_exit(self, user_input: str) -> bool:
        """
        Check if conversation should end based on user input.

        Args:
            user_input: User's message

        Returns:
            True if conversation should end, False otherwise
        """
        return is_exit_command(user_input)

    def get_exit_message(self) -> str:
        """
        Get the exit/goodbye message.

        Returns:
            Exit message string
        """
        self.conversation_active = False
        return EXIT_MESSAGE

    def get_next_question(self) -> Optional[str]:
        """
        Get the next information collection question.

        Returns:
            Next question string, or None if all information is collected
        """
        if self.current_field_index < len(CANDIDATE_INFO_FIELDS):
            return CANDIDATE_INFO_FIELDS[self.current_field_index]['prompt']
        return None

    def process_user_response(self, user_input: str) -> Tuple[str, bool]:
        """
        Process user response and determine next action.

        Args:
            user_input: User's message

        Returns:
            Tuple of (bot_response, should_continue)
        """
        user_input = sanitize_input(user_input)

        if self.should_exit(user_input):
            return self.get_exit_message(), False

        if self.current_field_index < len(CANDIDATE_INFO_FIELDS):
            return self._collect_candidate_info(user_input)
        elif not self.tech_questions_generated:
            return self._generate_technical_questions()
        else:
            return "All questions have been asked. Thank you for your time!", False

    def _collect_candidate_info(self, user_input: str) -> Tuple[str, bool]:
        """
        Collect candidate information step by step.

        Args:
            user_input: User's response

        Returns:
            Tuple of (bot_response, should_continue)
        """
        current_field = CANDIDATE_INFO_FIELDS[self.current_field_index]['field']

        validation_result = self._validate_field(current_field, user_input)

        if not validation_result[0]:
            return validation_result[1], True

        self.candidate_data[current_field] = validation_result[1]

        if current_field == 'tech_stack':
            self.candidate_data[current_field] = parse_tech_stack(user_input)

        self.current_field_index += 1

        if self.current_field_index < len(CANDIDATE_INFO_FIELDS):
            next_question = self.get_next_question()
            return f"Thank you! {next_question}", True
        else:
            return "Great! I have all the information I need. Let me generate some technical questions based on your tech stack...", True

    def _validate_field(self, field: str, value: str) -> Tuple[bool, str]:
        """
        Validate user input for specific field.

        Args:
            field: Field name being validated
            value: User input value

        Returns:
            Tuple of (is_valid, value_or_error_message)
        """
        if not value or not value.strip():
            return False, "I didn't quite understand that. Could you please rephrase?"

        if field == 'email':
            if not validate_email(value):
                return False, "That doesn't appear to be a valid email address. Could you please provide a valid email?"
            return True, value.strip()

        elif field == 'phone':
            if not validate_phone(value):
                return False, "That doesn't appear to be a valid phone number. Could you please provide a valid phone number?"
            return True, value.strip()

        elif field == 'experience':
            if not validate_experience(value):
                return False, "Please provide a valid number of years of experience (e.g., '5' or '2.5 years')."
            return True, value.strip()

        return True, value.strip()

    def _generate_technical_questions(self) -> Tuple[str, bool]:
        """
        Generate technical interview questions using Google Gemini.

        Returns:
            Tuple of (questions_string, should_continue)
        """
        if 'tech_stack' not in self.candidate_data or not self.candidate_data['tech_stack']:
            return "No tech stack was provided. Thank you for your time!", False

        tech_stack = self.candidate_data['tech_stack']

        if isinstance(tech_stack, list):
            tech_stack_str = ', '.join(tech_stack)
        else:
            tech_stack_str = str(tech_stack)

        try:
            prompt = TECHNICAL_QUESTION_GENERATION_PROMPT.format(tech_stack=tech_stack_str)

            full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt}"

            response = self.model.generate_content(full_prompt)

            questions = response.text

            self.tech_questions_generated = True

            intro = f"\nBased on your experience with {tech_stack_str}, here are some technical questions:\n\n"

            return intro + questions, False

        except Exception as e:
            error_msg = "I apologize, but I encountered an issue generating technical questions. Our team will follow up with you shortly."
            print(f"Error generating questions: {str(e)}")
            return error_msg, False

    def get_state(self) -> Dict:
        """
        Get current chatbot state for persistence.

        Returns:
            Dictionary containing current state
        """
        return {
            'current_field_index': self.current_field_index,
            'candidate_data': self.candidate_data,
            'conversation_active': self.conversation_active,
            'tech_questions_generated': self.tech_questions_generated
        }

    def set_state(self, state: Dict):
        """
        Restore chatbot state from saved data.

        Args:
            state: Dictionary containing saved state
        """
        self.current_field_index = state.get('current_field_index', 0)
        self.candidate_data = state.get('candidate_data', {})
        self.conversation_active = state.get('conversation_active', True)
        self.tech_questions_generated = state.get('tech_questions_generated', False)
