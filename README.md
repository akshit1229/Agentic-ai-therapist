AI Mental Health Therapist – SafeSpace

Your compassionate AI companion for emotional support, built with care and real-world tools. SafeSpace listens, understands, and responds with empathy — and knows when to escalate to emergency help.

Equipped with an AI agent architecture, specialist healthcare models (MedGemma), and life-saving tools like emergency calling via Twilio, SafeSpace is designed to support mental well-being — safely and responsibly.



🚀 Quick Start

Clone the repo and run:
```
git clone https://github.com/AIwithhassan/safespace-ai-therapist.git
```

# Setup UV :  

```
uv sync
```

That’s it. This command:

Creates a virtual environment (if needed)
Installs all dependencies from uv.lock
Sets up the full environment exactly as intended

# setup config file 
TWILIO_ACCOUNT_SID = ""

TWILIO_AUTH_TOKEN = "" 

TWILIO_FROM_NUMBER = ""  # your Twilio number

EMERGENCY_CONTACT = ""  # or your local emergency number 

GROQ_API_KEY=

# run fontend
uv run streamlit run frontend.py

# run backend
uv run backend/main.py
