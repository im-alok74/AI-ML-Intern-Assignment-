"""
TalentScout Hiring Assistant - Streamlit Application
Main application file for the AI-powered hiring chatbot interface.

Run with: streamlit run app.py
"""

import os
import streamlit as st
from dotenv import load_dotenv

from chatbot import HiringAssistant

load_dotenv()


def initialize_session_state():
    """
    Initialize Streamlit session state variables.
    All data is stored in-memory only for GDPR compliance.
    """
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if 'chatbot' not in st.session_state:
        api_key = os.getenv('GEMINI_API_KEY')

        if not api_key:
            st.error("GEMINI_API_KEY not found. Please set it in your .env file.")
            st.stop()

        st.session_state.chatbot = HiringAssistant(api_key)

    if 'conversation_active' not in st.session_state:
        st.session_state.conversation_active = True

    if 'initialized' not in st.session_state:
        greeting = st.session_state.chatbot.get_greeting()
        st.session_state.messages.append({"role": "assistant", "content": greeting})

        next_question = st.session_state.chatbot.get_next_question()
        if next_question:
            st.session_state.messages.append({"role": "assistant", "content": next_question})

        st.session_state.initialized = True


def render_chat_interface():
    """
    Render the chat interface with message history.
    """
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def handle_user_input():
    """
    Handle user input and generate bot response.
    """
    if not st.session_state.conversation_active:
        st.chat_input("Chat ended", disabled=True)
        return

    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response, should_continue = st.session_state.chatbot.process_user_response(prompt)

                st.markdown(response)

                st.session_state.messages.append({"role": "assistant", "content": response})

                if not should_continue:
                    st.session_state.conversation_active = False
                    st.rerun()


def render_sidebar():
    """
    Render sidebar with application information and instructions.
    """
    with st.sidebar:
        st.header("About TalentScout")

        st.markdown("""
        **TalentScout** is an AI-powered hiring assistant that conducts initial candidate screening.

        ### How it works:
        1. The chatbot will ask for basic information
        2. You'll be asked about your tech stack
        3. Technical questions will be generated based on your skills

        ### Tips:
        - Answer one question at a time
        - Be specific about your tech stack
        - Type 'exit' or 'quit' to end the conversation

        ### Privacy Notice:
        All data is processed in-memory only and is not stored persistently.
        Your information is GDPR-compliant and secure.
        """)

        st.divider()

        if st.button("Reset Conversation", type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        st.divider()

        st.caption("Powered by Google Gemini AI")
        st.caption("Built with Streamlit")


def main():
    """
    Main application entry point.
    """
    st.set_page_config(
        page_title="TalentScout Hiring Assistant",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("🎯 TalentScout Hiring Assistant")
    st.subheader("Initial Candidate Screening Chat")

    st.markdown("---")

    initialize_session_state()

    render_sidebar()

    render_chat_interface()

    handle_user_input()

    if not st.session_state.conversation_active:
        st.info("💬 Conversation has ended. Click 'Reset Conversation' in the sidebar to start over.")


if __name__ == "__main__":
    main()
