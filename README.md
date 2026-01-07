# TalentScout - AI Hiring Assistant Chatbot

An intelligent, context-aware hiring assistant chatbot built for TalentScout, a fictional recruitment agency. This production-ready application conducts initial candidate screening, collects candidate information systematically, and generates personalized technical interview questions based on the candidate's tech stack.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation Instructions](#installation-instructions)
- [Usage Guide](#usage-guide)
- [Prompt Engineering Explanation](#prompt-engineering-explanation)
- [Architecture & Design Decisions](#architecture--design-decisions)
- [Data Privacy & GDPR Compliance](#data-privacy--gdpr-compliance)
- [Challenges & Solutions](#challenges--solutions)
- [Demo Instructions](#demo-instructions)
- [Project Structure](#project-structure)
- [License](#license)

---

## Project Overview

TalentScout is an AI-powered hiring assistant designed to streamline the initial candidate screening process. The chatbot engages candidates in a professional conversation, collects essential information step-by-step, and generates relevant technical interview questions based on their declared expertise.

**Key Objectives:**
- Automate initial candidate screening
- Maintain professional and context-aware conversations
- Generate high-quality technical interview questions
- Demonstrate advanced prompt engineering techniques
- Ensure data privacy and GDPR compliance

---

## Features

### Core Functionality

1. **Automated Greeting**
   - Welcomes candidates with a professional introduction
   - Sets clear expectations for the screening process

2. **Step-by-Step Information Collection**
   - Collects the following information sequentially:
     - Full Name
     - Email Address
     - Phone Number
     - Years of Experience
     - Desired Position(s)
     - Current Location
     - Tech Stack
   - Never skips or repeats questions
   - Validates input at each step

3. **Intelligent Tech Stack Parsing**
   - Accepts both comma-separated and space-separated inputs
   - Examples: "Python, Django, SQL" or "Python Django SQL"
   - Normalizes and stores technologies cleanly

4. **AI-Powered Technical Question Generation**
   - Generates 3-5 targeted questions per technology
   - Question types include:
     - Basic conceptual questions
     - Intermediate implementation questions
     - Scenario-based practical questions
   - Questions are grouped by technology for clarity

5. **Context Awareness**
   - Maintains full conversation history
   - Ensures smooth transitions between screening stages
   - Stays focused on hiring objectives

6. **Graceful Exit Handling**
   - Detects exit keywords: exit, quit, bye, thank you
   - Provides professional closing message
   - Disables further input after conversation ends

7. **Robust Error Handling**
   - Validates email format
   - Validates phone number format
   - Validates years of experience
   - Handles unclear responses professionally

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.8+ |
| **Frontend** | Streamlit |
| **LLM Provider** | Google Gemini Pro |
| **Storage** | In-memory (Streamlit session_state) |
| **Environment** | python-dotenv |

---

## Installation Instructions

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd talentscout-hiring-assistant
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_actual_api_key_here
```

### Step 5: Run the Application

```bash
streamlit run app.py
```

The application will open automatically in your default browser at `http://localhost:8501`.

---

## Usage Guide

### Starting a Conversation

1. Launch the application using `streamlit run app.py`
2. The chatbot will automatically greet you and ask the first question
3. Answer each question one at a time
4. Provide your tech stack when prompted (e.g., "Python, Django, PostgreSQL")

### During the Conversation

- **Answer questions naturally**: The chatbot validates inputs and provides feedback
- **Tech stack format**: Use commas or spaces to separate technologies
- **Exit anytime**: Type "exit", "quit", "bye", or "thank you" to end the conversation

### After Information Collection

- The chatbot will generate technical interview questions based on your tech stack
- Questions are organized by technology
- Each technology receives 3-5 targeted questions ranging from basic to scenario-based

### Resetting the Conversation

- Click the "Reset Conversation" button in the sidebar
- This clears all data and starts a fresh session

---

## Prompt Engineering Explanation

This project demonstrates advanced prompt engineering techniques to ensure controlled, professional, and context-aware AI behavior.

### 1. System Prompt Design

```python
SYSTEM_PROMPT = """You are TalentScout, a professional hiring assistant chatbot.
Your role is limited strictly to candidate screening and technical assessment.
You must remain concise, professional, polite, and hiring-focused.
You must not answer technical questions or deviate from recruitment tasks."""
```

**Purpose:**
- Establishes the AI's role and boundaries
- Prevents off-topic conversations
- Maintains professional tone throughout

### 2. Information Collection Prompt

```python
INFORMATION_COLLECTION_PROMPT = """Ask only ONE required candidate detail at a time.
Wait for the user's response before proceeding.
Do NOT ask technical questions yet."""
```

**Purpose:**
- Enforces sequential information gathering
- Prevents the AI from skipping ahead
- Ensures complete data collection

### 3. Technical Question Generation Prompt

The technical question prompt is structured to produce high-quality, diverse interview questions:

```python
TECHNICAL_QUESTION_GENERATION_PROMPT = """Generate technical interview questions...

Question structure per technology:
1. One basic conceptual question
2. Two intermediate implementation questions
3. One scenario-based or practical question
"""
```

**Key Features:**
- Specifies exact question counts (3-5 per technology)
- Defines difficulty levels
- Requires scenario-based questions
- Explicitly prohibits including answers
- Ensures questions are grouped by technology

### 4. Context Control

The chatbot maintains strict context awareness through:
- **State management**: Tracks which field is currently being collected
- **Validation gates**: Only proceeds after successful validation
- **Sequential flow**: Never asks technical questions before collecting tech stack

### 5. Fallback Handling

When user input is unclear:
```python
"I didn't quite understand that. Could you please rephrase?"
```

This simple, professional response keeps the conversation on track without frustrating the user.

---

## Architecture & Design Decisions

### Modular Design

The application follows a clean, modular architecture:

```
app.py          # Streamlit UI and main application logic
chatbot.py      # Conversation flow controller and state management
prompts.py      # All prompt templates and conversation scripts
utils.py        # Input validation and parsing utilities
```

**Benefits:**
- Easy to test individual components
- Clear separation of concerns
- Simple to extend or modify functionality
- Maintainable codebase

### State Management

All conversation state is managed through Streamlit's `session_state`:

```python
st.session_state.chatbot         # HiringAssistant instance
st.session_state.messages        # Chat history
st.session_state.conversation_active  # Conversation status
```

**Benefits:**
- No database setup required
- GDPR-compliant (no persistent storage)
- Fast and responsive
- Easy to reset/clear

### Validation Strategy

Multi-layer validation approach:

1. **Input sanitization**: Remove potentially harmful characters
2. **Format validation**: Email, phone, experience format checks
3. **Logical validation**: Experience years between 0-50
4. **User feedback**: Clear error messages for invalid inputs

### LLM Integration

Google Gemini Pro is used exclusively for technical question generation:

- **Why only for questions?**: To maintain control and predictability for structured data collection
- **Prompt design**: Carefully crafted to produce consistent, high-quality output
- **Error handling**: Graceful fallback if API fails

---

## Data Privacy & GDPR Compliance

### Privacy-First Architecture

TalentScout is designed with data privacy as a core principle:

1. **No Persistent Storage**
   - All data is stored in-memory using Streamlit session_state
   - No databases, files, or external storage systems
   - Data is automatically cleared when the browser session ends

2. **GDPR Compliance**
   - Right to be forgotten: Achieved through session-based storage
   - Data minimization: Only collects necessary information
   - Purpose limitation: Data used only for screening purposes
   - Transparency: Clear privacy notice in the sidebar

3. **Data Security**
   - Input sanitization prevents injection attacks
   - API keys stored securely in environment variables
   - No logging of personal information

4. **User Control**
   - Users can exit the conversation at any time
   - "Reset Conversation" button provides immediate data clearing
   - Clear indication when conversation has ended

### Compliance Notes

```python
# All data processing happens in-memory only
# No persistent storage ensures GDPR compliance
candidate_data = {}  # Stored in session_state, cleared on exit
```

---

## Challenges & Solutions

### Challenge 1: Maintaining Sequential Flow

**Problem**: Ensuring the chatbot asks questions one at a time without skipping or repeating.

**Solution**:
- Implemented a `current_field_index` tracker
- Each field is validated before incrementing the index
- Prompts explicitly instruct the AI to ask only one question at a time

### Challenge 2: Tech Stack Input Flexibility

**Problem**: Users might input tech stacks in various formats (commas, spaces, mixed).

**Solution**:
```python
def parse_tech_stack(tech_stack_input: str) -> List[str]:
    if ',' in tech_stack_input:
        technologies = [tech.strip() for tech in tech_stack_input.split(',')]
    else:
        technologies = [tech.strip() for tech in tech_stack_input.split()]
    return technologies
```

### Challenge 3: Preventing Off-Topic Conversations

**Problem**: LLMs can be prone to going off-topic or providing unsolicited information.

**Solution**:
- Strong system prompt establishing role boundaries
- Explicit instructions to not answer technical questions
- Context control through state management

### Challenge 4: Graceful Exit Detection

**Problem**: Users might want to exit using various phrases.

**Solution**:
```python
exit_keywords = ['exit', 'quit', 'bye', 'thank you', 'thanks']
return any(keyword in user_input_lower for keyword in exit_keywords)
```

### Challenge 5: Input Validation Without Frustration

**Problem**: Strict validation can frustrate users with false negatives.

**Solution**:
- Flexible phone number validation (accepts various formats)
- Clear, helpful error messages
- Multiple acceptable formats for experience ("5", "5 years", "5yrs")

---

## Demo Instructions

### Basic Usage Demo

1. **Start the application**:
   ```bash
   streamlit run app.py
   ```

2. **Follow the conversation flow**:
   - Chatbot greets you
   - Provide your name: "John Doe"
   - Provide email: "john.doe@example.com"
   - Provide phone: "+1-555-123-4567"
   - Provide experience: "5 years"
   - Provide position: "Senior Backend Developer"
   - Provide location: "San Francisco, CA"
   - Provide tech stack: "Python, Django, PostgreSQL, Docker"

3. **Observe technical question generation**:
   - Chatbot will generate 3-5 questions for each technology
   - Questions cover conceptual, implementation, and scenario-based topics

4. **Exit the conversation**:
   - Type "thank you" or "exit"
   - Observe the professional closing message
   - Notice the input is disabled

### Testing Exit Functionality

1. At any point during information collection, type "exit"
2. Confirm the conversation ends gracefully
3. Check that further input is disabled

### Testing Validation

1. Try entering an invalid email: "notanemail"
2. Observe the validation error and helpful message
3. Enter a valid email to proceed

### Testing Reset

1. Complete a full conversation
2. Click "Reset Conversation" in the sidebar
3. Confirm the conversation starts fresh

---

## Project Structure

```
talentscout-hiring-assistant/
├── app.py                  # Main Streamlit application
├── chatbot.py              # Conversation controller and logic
├── prompts.py              # All prompt templates
├── utils.py                # Helper functions and validators
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

### File Descriptions

**app.py**
- Streamlit UI implementation
- Chat interface using `st.chat_message`
- Session state initialization
- User input handling
- Sidebar with instructions and reset button

**chatbot.py**
- `HiringAssistant` class
- Conversation state management
- Information collection logic
- Technical question generation
- Exit handling

**prompts.py**
- System prompt
- Information collection prompt
- Technical question generation prompt
- Greeting and exit messages
- Field definitions

**utils.py**
- `parse_tech_stack()`: Normalize tech stack input
- `validate_email()`: Email format validation
- `validate_phone()`: Phone number validation
- `validate_experience()`: Experience validation
- `is_exit_command()`: Exit keyword detection
- `sanitize_input()`: Input sanitization

---

## License

This project is created for educational and demonstration purposes as part of an AI/ML internship assignment.

---

## Contact

For questions or issues, please contact the development team or open an issue in the repository.

---

**Built with precision for TalentScout** | Powered by Google Gemini AI | Developed with Streamlit
#   A I - M L - I n t e r n - A s s i g n m e n t -  
 #   A I - M L - I n t e r n - A s s i g n m e n t -  
 