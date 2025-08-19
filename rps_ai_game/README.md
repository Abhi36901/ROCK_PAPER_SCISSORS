# Rock–Paper–Scissors with Learning AI (Flask + JS)

## Quickstart
```bash
# 1) Create and activate a virtual environment (recommended)
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 2) Install deps
pip install -r requirements.txt

# 3) Run the server
python app.py
# or
# flask --app app run

# 4) Open in your browser
http://127.0.0.1:5000
```

## Notes
- The AI uses a first-order Markov model with epsilon-greedy randomness.
- Memory persists in `data/ai_memory.json`.
- Click **Reset Memory** to clear stats/history.
