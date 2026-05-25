# AI-Based Nine Men's Morris Game

A fully functional, desktop-based Nine Men's Morris game built with Python and Pygame. This project was developed as a semester project for an AI course. It features both Human vs. Human and Human vs. AI modes, with the AI powered by the Minimax algorithm and Alpha-Beta pruning.

## Features
- **Responsive UI:** Minimalist and modern Pygame interface that supports window resizing.
- **Complete Ruleset:** Implements all phases of Nine Men's Morris (Placing, Moving, and Flying).
- **Mill Mechanics:** Robust logic to detect "mills" (three pieces in a row) and enforce valid piece removals.
- **AI Opponent:** Play against an AI agent utilizing Minimax with Alpha-Beta pruning.
- **Difficulty Levels:** Choose between Easy, Medium, and Hard AI difficulties.
- **Visual Feedback:** Highlights selected pieces, valid move destinations, and removable opponent pieces.

## Prerequisites
- Python 3.x
- Pygame (`pip install pygame`)

## Installation and Execution
1. Clone or download the repository.
2. Ensure you have `pygame` installed. You can install it via terminal:
   ```bash
   pip install pygame
   ```
3. Run the main file to start the game:
   ```bash
   python main.py
   ```

## Rules of Nine Men's Morris
The game is played on a board consisting of 24 intersections (nodes). Each player has 9 pieces.

1. **Phase 1: Placing** 
   Players take turns placing their pieces onto empty nodes. If a player places three of their pieces in a contiguous straight line (a "Mill"), they must remove one of the opponent's pieces. An opponent's piece that is part of a mill cannot be removed unless no other pieces are available.

2. **Phase 2: Moving**
   Once all 9 pieces are placed, players take turns moving one of their pieces to an adjacent empty node. Forming a mill again allows the removal of an opponent's piece.

3. **Phase 3: Flying**
   When a player is reduced to exactly 3 pieces, their pieces gain the ability to "fly" to *any* empty node on the board, not just adjacent ones.

**Winning:**
A player wins if their opponent is reduced to 2 pieces (making it impossible to form a mill) OR if their opponent has no valid moves left.

## AI Implementation
The AI uses the **Minimax Algorithm** with **Alpha-Beta Pruning** to drastically reduce the number of nodes evaluated in the search tree. 
- The **Easy** difficulty searches to a shallow depth (2).
- The **Medium** difficulty searches to a standard depth (3).
- The **Hard** difficulty searches deeper (4), planning multiple steps ahead.
- The **Heuristic Evaluation Function** scores board states based primarily on the piece difference between the AI and the Human player. More pieces equal a higher score.

## Code Structure
- `constants.py`: Stores colors, window size, and player constants.
- `board.py`: Contains the `Board` class managing the graph adjacency list and mill logic.
- `game.py`: Contains the `GameState` class handling turns, phases, and win logic.
- `ai.py`: Implements the `MinimaxAI` class and its evaluation functions.
- `ui.py`: Manages all Pygame rendering and user interactions.
- `main.py`: The entry point for the game.
