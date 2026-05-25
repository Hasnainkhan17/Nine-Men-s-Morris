from game import GameState, PHASE_PLACING, PHASE_MOVING_FLYING
from ai import MinimaxAI
from constants import PLAYER1, PLAYER2

def run_headless_test():
    state = GameState()
    ai1 = MinimaxAI(ai_player=PLAYER1, difficulty='easy')
    ai2 = MinimaxAI(ai_player=PLAYER2, difficulty='easy')

    print("Starting Headless Game Test...")
    moves_made = 0
    max_moves = 50 # Just run a few turns to check for crashes

    while not state.game_over and moves_made < max_moves:
        current_ai = ai1 if state.turn == PLAYER1 else ai2
        
        print(f"Turn: {state.turn}, Phase: {state.phase}, Remove Mode: {state.remove_mode}")
        
        best_next_state = current_ai.get_best_move(state)
        
        if best_next_state is None:
            print("No valid moves found, checking game over.")
            state.check_game_over()
            break
            
        state = best_next_state
        moves_made += 1
        
    print(f"Test completed after {moves_made} moves. Game Over: {state.game_over}, Winner: {state.winner}")
    print("Test passed successfully without exceptions!")

if __name__ == "__main__":
    run_headless_test()
