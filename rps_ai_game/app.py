from __future__ import annotations
from flask import Flask, render_template, request, jsonify, session
import random
import json, os, secrets, threading, time
from typing import Dict, List

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(APP_DIR, "data", "ai_memory.json")

app = Flask(__name__)
# Secret key for sessions (per run). For production, set from env.
app.secret_key = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(16))

lock = threading.Lock()

MOVES = ["rock", "paper", "scissors"]

def counter_of(move: str) -> str:
    if move == "rock": return "paper"
    if move == "paper": return "scissors"
    return "rock"

class MarkovAI:
    def __init__(self, order: int = 1, epsilon: float = 0.15):
        # order = how many previous user moves to condition on
        # epsilon = randomization factor so the AI doesn't feel robotic
        self.order = order
        self.epsilon = epsilon
        self.history: List[str] = []
        # transition_counts maps "key string" -> {next_move -> count}
        self.transition_counts: Dict[str, Dict[str, int]] = {}
        self.stats = {"wins": 0, "losses": 0, "ties": 0}

    @staticmethod
    def _key_from_seq(seq: List[str]) -> str:
        return "|".join(seq) if seq else ""

    def predict_next_user_move(self) -> str:
        # If not enough history, random
        if len(self.history) < self.order:
            return random.choice(MOVES)
        key = self._key_from_seq(self.history[-self.order:])
        next_map = self.transition_counts.get(key)
        if not next_map:
            return random.choice(MOVES)
        # Choose the most frequent next move
        return max(next_map, key=next_map.get)

    def probs_for_next(self) -> Dict[str, float]:
        # Returns probability-like weights for UI
        if len(self.history) < self.order:
            return {m: 1/3 for m in MOVES}
        key = self._key_from_seq(self.history[-self.order:])
        next_map = self.transition_counts.get(key, {})
        total = sum(next_map.values())
        if total == 0:
            return {m: 1/3 for m in MOVES}
        return {m: next_map.get(m, 0) / total for m in MOVES}

    def choose_ai_move(self) -> str:
        # Epsilon-greedy: sometimes play random
        if random.random() < self.epsilon:
            return random.choice(MOVES)
        predicted_user = self.predict_next_user_move()
        return counter_of(predicted_user)

    def update_with_user_move(self, user_move: str):
        # Update transition counts using last 'order' moves to key
        if self.order >= 1 and len(self.history) >= self.order:
            key = self._key_from_seq(self.history[-self.order:])
            if key not in self.transition_counts:
                self.transition_counts[key] = {}
            self.transition_counts[key][user_move] = self.transition_counts[key].get(user_move, 0) + 1
        # Append to history after updating transitions (conditioning on *previous* moves)
        self.history.append(user_move)

    def to_dict(self) -> Dict:
        return {
            "order": self.order,
            "epsilon": self.epsilon,
            "history": self.history,
            "transition_counts": self.transition_counts,
            "stats": self.stats,
        }

    @classmethod
    def from_dict(cls, d: Dict) -> "MarkovAI":
        ai = cls(order=d.get("order", 1), epsilon=d.get("epsilon", 0.15))
        ai.history = d.get("history", [])
        ai.transition_counts = d.get("transition_counts", {})
        ai.stats = d.get("stats", {"wins": 0, "losses": 0, "ties": 0})
        return ai

def load_ai() -> MarkovAI:
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, "r") as f:
                d = json.load(f)
                return MarkovAI.from_dict(d)
        except Exception:
            pass
    return MarkovAI(order=int(os.environ.get("AI_ORDER", "1")), epsilon=float(os.environ.get("AI_EPSILON", "0.15")))

def save_ai(ai: MarkovAI):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w") as f:
        json.dump(ai.to_dict(), f, indent=2)

# Initialize AI
AI = load_ai()

@app.route("/")
def index():
    # Ensure a session exists (for future multi-user features)
    session.setdefault("sid", secrets.token_hex(8))
    return render_template("index.html")

@app.route("/play", methods=["POST"])
def play():
    data = request.get_json(force=True)
    user = data.get("move")
    if user not in MOVES:
        return jsonify({"error": "Invalid move"}), 400

    with lock:
        # Choose AI move based on current history (before seeing new move)
        ai_choice = AI.choose_ai_move()

        # Determine result
        if user == ai_choice:
            outcome = "tie"
            AI.stats["ties"] += 1
        elif (user == "rock" and ai_choice == "scissors") or \
             (user == "paper" and ai_choice == "rock") or \
             (user == "scissors" and ai_choice == "paper"):
            outcome = "user_win"
            AI.stats["losses"] += 1   # AI lost
        else:
            outcome = "ai_win"
            AI.stats["wins"] += 1

        # For UI: what did the AI think you'd play?
        predicted_user = AI.predict_next_user_move()
        probs = AI.probs_for_next()

        # Now update AI with the actual user move (learning step)
        AI.update_with_user_move(user)
        save_ai(AI)

    # Construct a human-friendly result line
    result_text = "It's a tie!" if outcome == "tie" else ("You win!" if outcome == "user_win" else "AI wins!")

    return jsonify({
        "user": user,
        "ai": ai_choice,
        "result": result_text,
        "outcome": outcome,
        "predicted_user_move": predicted_user,
        "probs": probs,
        "stats": AI.stats
    })

@app.route("/reset", methods=["POST"])
def reset():
    global AI
    with lock:
        AI = MarkovAI(order=AI.order, epsilon=AI.epsilon)
        save_ai(AI)
    return jsonify({"ok": True, "message": "AI memory and stats reset."})

@app.route("/state", methods=["GET"])
def state():
    with lock:
        return jsonify({
            "history_len": len(AI.history),
            "stats": AI.stats,
            "order": AI.order,
            "epsilon": AI.epsilon,
            "last_key_probs": AI.probs_for_next(),
        })

if __name__ == "__main__":
    # You can set host="0.0.0.0" to access from other devices on LAN
    app.run(debug=True)
