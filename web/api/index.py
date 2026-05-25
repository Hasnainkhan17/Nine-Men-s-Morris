from flask import Flask, request, jsonify
from game_logic import GameState, MinimaxAI

app = Flask(__name__)

@app.route('/api/ai-move', methods=['POST'])
def get_ai_move():
    data = request.json
    state_dict = data.get('state')
    difficulty = data.get('difficulty', 'medium')
    
    if not state_dict:
        return jsonify({"error": "No state provided"}), 400
        
    # Reconstruct the game state
    state = GameState.from_dict(state_dict)
    
    # Check if game is already over
    if state.game_over:
        return jsonify({"state": state.to_dict()})
        
    # Get the AI's move
    ai = MinimaxAI(ai_player=state.turn, difficulty=difficulty)
    best_next_state = ai.get_best_move(state)
    
    if best_next_state:
        # Check if the move ended the game
        best_next_state.check_game_over()
        return jsonify({"state": best_next_state.to_dict()})
    else:
        # No moves possible (should have been caught by game_over, but fallback)
        state.check_game_over()
        return jsonify({"state": state.to_dict()})

# Vercel needs this
if __name__ == '__main__':
    app.run(debug=True)
