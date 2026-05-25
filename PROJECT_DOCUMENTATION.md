# Project Documentation: AI-Based Nine Men's Morris

**Course:** Artificial Intelligence Semester Project  
**Developed by:** Muhammad Hasnain & Sundas Gulzar

---

## 1. Project Overview
This project is an implementation of the classic strategy board game **Nine Men's Morris** with a heavy focus on Artificial Intelligence. The application is built as a highly responsive, modern Web Application (Next.js/React) backed by a Python serverless architecture that handles all complex AI decision-making. 

The core objective of this project was to model the game environment programmatically and implement a robust, unbeatable (or highly competitive) AI opponent using the **Minimax Algorithm** optimized with **Alpha-Beta Pruning**.

---

## 2. Artificial Intelligence Implementation

The intelligence of the AI agent is encapsulated in the Python backend (`api/game_logic.py` and `desktop/ai.py`). The problem is modeled as a zero-sum, perfect information game.

### 2.1 State Space Representation
The board consists of 24 interconnected intersections (nodes). The state of the game is represented as:
- **Board Array:** A 24-element array where each index corresponds to a specific node on the board. Each node can be `EMPTY (0)`, `PLAYER1 (1)`, or `PLAYER2 (2)`.
- **Game Phase:** The game transitions between `PHASE_PLACING` (all 9 pieces must be dropped) and `PHASE_MOVING_FLYING` (pieces slide to adjacent nodes, or "fly" if only 3 pieces remain).
- **Mill Detection:** A predefined list of 16 winning alignments (mills). When a player forms a mill, they enter `remove_mode` to capture an opponent's piece.

### 2.2 The Minimax Algorithm
To allow the AI to "think ahead," we implemented the **Minimax Algorithm**. The AI evaluates the game tree by simulating all possible valid moves (and subsequent opponent counter-moves) up to a certain depth.
- **Maximizing Player:** The AI agent, which seeks to maximize the evaluation score.
- **Minimizing Player:** The Human opponent, whom the AI assumes will play optimally to minimize the AI's score.

Because Nine Men's Morris has a very high branching factor (especially during the Moving phase when pieces can slide, and the Placing phase where there are up to 24 empty spots), generating the entire game tree is computationally impossible. Thus, we use a **Depth-Limited Minimax**.

### 2.3 Alpha-Beta Pruning Optimization
To solve the performance bottleneck of standard Minimax, we integrated **Alpha-Beta Pruning**.
- **Alpha ($\alpha$):** The best (highest) value the AI can guarantee at the current level or above.
- **Beta ($\beta$):** The best (lowest) value the Human can guarantee at the current level or above.

During the recursive tree search, if the algorithm discovers a branch that is demonstrably worse than a previously examined branch (i.e., $\beta \le \alpha$), it **prunes** (cuts off) the rest of that branch. 
* **Impact:** This optimization reduces the number of nodes evaluated by almost 50% in best-case scenarios, allowing the AI to search deeper into the game tree within the same time limit, resulting in much smarter moves without UI lag.

### 2.4 Heuristic Evaluation Function
When the Minimax algorithm reaches its maximum depth, it cannot know the final outcome of the game (Win/Loss). Instead, it uses a **Heuristic Evaluation Function** to score the "goodness" of that board state.

Our evaluation function is defined as:
```python
def evaluate(self, state):
    if state.game_over:
        return float('inf') if state.winner == self.ai_player else float('-inf')
    
    ai_pieces = len(state.board.get_player_pieces(self.ai_player))
    human_pieces = len(state.board.get_player_pieces(self.human_player))
    
    return (ai_pieces - human_pieces) * 10
```
**Heuristic Logic:**
1. **Terminal States:** If a state results in an AI win, it returns $+\infty$. If it results in a Human win, it returns $-\infty$.
2. **Material Advantage:** The primary metric for a non-terminal state is the difference in piece count. By multiplying the difference by a weight (`10`), the AI is heavily incentivized to form Mills (which removes a human piece, increasing the score) and heavily discouraged from allowing the human to form Mills.

### 2.5 Difficulty Scaling
The difficulty of the AI is directly controlled by manipulating the `max_depth` of the Minimax search tree:
- **Easy (Depth 2):** The AI only looks 2 turns ahead. It will capture pieces if immediately obvious but is prone to falling for simple traps.
- **Medium (Depth 3):** The AI looks 3 turns ahead. It can anticipate the human's immediate counter-attacks.
- **Hard (Depth 4):** The AI looks 4 turns ahead. Combined with Alpha-Beta pruning, it plays a highly aggressive and defensive game, intentionally setting up double-mills.

---

## 3. Technology Stack & Architecture
While the AI relies on pure mathematics and computer science fundamentals, the delivery mechanism uses modern engineering:
- **Backend (AI Engine):** Python 3.14 (Flask Serverless API)
- **Frontend (UI/UX):** TypeScript, React, Next.js, Tailwind CSS
- **Deployment:** Vercel (CI/CD Pipeline)

The frontend maintains instantaneous optimistic state for UI feedback, but offloads all heavy Minimax tree-search computations to the Python backend via secure HTTP POST requests.

---
## 4. Conclusion
This project successfully demonstrates the power of adversarial search algorithms in perfect-information games. By implementing Alpha-Beta Pruning, we transformed a sluggish Minimax tree into a rapid, highly intelligent opponent capable of running efficiently in a serverless web environment.
