# TalentScout - Quick Start Guide

Get up and running with the TalentScout AI Hiring Assistant in 5 minutes.

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

## Installation

```bash
# 1. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 4. Run the application
streamlit run app.py
```

## Quick Test

Once the application is running:

1. The chatbot will greet you automatically
2. Answer the questions step by step:
   - Name: "John Doe"
   - Email: "john.doe@example.com"
   - Phone: "+1-555-123-4567"
   - Experience: "5 years"
   - Position: "Backend Developer"
   - Location: "San Francisco, CA"
   - Tech Stack: "Python, Django, PostgreSQL"

3. Watch as the AI generates technical interview questions
4. Type "exit" to end the conversation

## Validation

Run the structure validation test:

```bash
python3 test_structure.py
```

All tests should pass with green checkmarks.

## Troubleshooting

**Issue**: "GEMINI_API_KEY not found"
- Solution: Make sure you created a `.env` file and added your API key

**Issue**: "ModuleNotFoundError"
- Solution: Activate the virtual environment and install requirements

**Issue**: "Port already in use"
- Solution: Streamlit will automatically find an available port

## Features to Test

1. **Sequential Information Collection**: Each question appears only after the previous is answered
2. **Input Validation**: Try entering invalid email/phone to see validation in action
3. **Exit Handling**: Type "exit" or "thank you" at any time
4. **Tech Stack Flexibility**: Try both "Python, Django" and "Python Django" formats
5. **Technical Questions**: Generated dynamically based on your tech stack

## Project Structure

```
talentscout-hiring-assistant/
├── app.py                  # Streamlit UI
├── chatbot.py              # Conversation controller
├── prompts.py              # Prompt templates
├── utils.py                # Helper functions
├── requirements.txt        # Dependencies
├── .env.example            # Environment template
└── README.md               # Full documentation
```

## Support

For detailed documentation, see [README.md](README.md)

For questions or issues, please refer to the project documentation or contact the development team.

---

**Ready to go!** Just run `streamlit run app.py` and start screening candidates.
