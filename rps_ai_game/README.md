# Rock-Paper-Scissors AI

An interactive Rock-Paper-Scissors game featuring an adaptive AI opponent that uses a **Markov Chain–based prediction model** to analyze player behavior and make probability-driven decisions.

## Overview

This project implements a Rock-Paper-Scissors game with an AI opponent that learns from the player's move history. Instead of relying entirely on random choices, the AI tracks transitions between consecutive player moves and uses these patterns to predict the player's next move.

The predicted move is then used to select a counter-move, making the AI adaptive to recurring patterns in gameplay.

## Features

- **Adaptive AI:** Learns from the player's move history during gameplay.
- **Markov Chain Model:** Models transitions between player moves to estimate likely next moves.
- **Probability-Based Predictions:** Uses observed transition probabilities to guide the AI's decisions.
- **Interactive Gameplay:** Allows users to play multiple rounds against the AI.
- **Web-Based Interface:** Built with HTML and CSS for a simple and accessible user experience.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Game logic and AI implementation |
| Markov Chain Model | Player behavior modeling and move prediction |
| HTML | Game interface structure |
| CSS | Interface styling and layout |

## How It Works

The AI uses a Markov chain approach to identify patterns in the player's move sequence.

1. **Collect Moves:** The game records the player's moves across consecutive rounds.
2. **Track Transitions:** It maintains information about transitions between moves, such as Rock → Paper or Scissors → Rock.
3. **Estimate Probabilities:** The model uses observed transitions to estimate the likelihood of the player's next move.
4. **Predict the Next Move:** The AI selects a likely next move based on the learned transition patterns.
5. **Counter the Prediction:** The AI chooses the move that defeats its predicted player move.
6. **Update the Model:** As additional rounds are played, the transition information is updated to reflect the player's behavior.

This approach allows the AI to adapt to repetitive or predictable strategies rather than following a purely random policy.

## Performance

The AI achieved a **reported win rate of approximately 65–70%** during iterative testing and logic refinement.

Actual performance depends on the player's strategy, the number of rounds played, and how consistently the player exhibits exploitable patterns. This result should be interpreted as an observed performance figure rather than a guaranteed win rate against all strategies.

## Getting Started

### Prerequisites

- Python 3.x
- A modern web browser
- The project source files

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
   ```

2. Navigate to the project directory:

   ```bash
   cd YOUR-REPOSITORY
   ```

3. Install any dependencies listed in `requirements.txt`, if applicable:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Python application using its entry-point file. For example, if the main file is `app.py`:

   ```bash
   python app.py
   ```

5. Open the local URL displayed by the application in your browser, if it uses a web server.

**Note:** Update the commands above to match your actual project structure. If the game is a static HTML/CSS interface without a Python web server, open the HTML entry-point file directly in your browser.

## Project Structure

A possible project structure is shown below. Adjust the filenames to match your repository.

```text
Rock-Paper-Scissors-AI/
├── app.py              # Python application and game logic
├── templates/
│   └── index.html      # Game interface
├── static/
│   └── style.css       # Styling
├── requirements.txt    # Python dependencies, if required
└── README.md
```

## Learning Outcomes

Through this project, I explored:

- Applying Markov chains to sequential decision-making problems.
- Estimating transition probabilities from observed data.
- Designing adaptive algorithms based on gameplay history.
- Integrating Python game logic with a web-based interface.
- Refining prediction logic through iterative testing.

## Future Improvements

- Experiment with higher-order Markov models to capture longer sequences of player behavior.
- Add visual statistics for move frequencies, predictions, and win rates.
- Compare the Markov chain approach against a random baseline.
- Evaluate performance over larger test sets and against different player strategies.
- Improve prediction handling when insufficient historical data is available.

## Author

**Abhijeet Udgata**

Computer Science and Engineering Undergraduate

---

*Built as a project exploring probabilistic modeling, adaptive algorithms, and interactive web development.*
