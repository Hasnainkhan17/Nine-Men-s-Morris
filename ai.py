import math
from constants import PLAYER1, PLAYER2, EMPTY
from game import PHASE_PLACING

class MinimaxAI:
    def __init__(self, ai_player=PLAYER2, difficulty='medium'):
        self.ai_player = ai_player
        self.human_player = PLAYER1 if ai_player == PLAYER2 else PLAYER2
        
        # Adjust depth based on difficulty
        if difficulty == 'easy':
            self.max_depth = 2
        elif difficulty == 'hard':
            self.max_depth = 4
        else:
            self.max_depth = 3 # medium

    def evaluate(self, state):
        """Heuristic evaluation function for the board state."""
        if state.game_over:
            if state.winner == self.ai_player:
                return float('inf')
            elif state.winner == self.human_player:
                return float('-inf')
            else:
                return 0

        # Features to evaluate
        ai_pieces = len(state.board.get_player_pieces(self.ai_player))
        human_pieces = len(state.board.get_player_pieces(self.human_player))
        
        # A simple but effective heuristic:
        # Score = (AI pieces - Human pieces) * 10
        score = (ai_pieces - human_pieces) * 10
        
        # Add points for potential mills or board dominance here if needed.
        # This basic heuristic is often enough combined with a depth of 3-4.
        
        return score

    def get_all_possible_moves(self, state, player):
        """Generates all possible valid next states for the given player."""
        moves = [] # list of (action_desc, next_state) tuples
        
        if state.remove_mode:
            # Must remove an opponent's piece
            opponent = PLAYER2 if player == PLAYER1 else PLAYER1
            removable = state.board.get_removable_pieces(opponent)
            for r_node in removable:
                new_state = state.clone()
                # Apply remove logic similar to handle_click
                new_state.board.remove_piece(r_node)
                new_state.remove_mode = False
                new_state.switch_turn()
                moves.append((f"remove_{r_node}", new_state))
            return moves

        if state.phase == PHASE_PLACING:
            empty_nodes = state.board.get_all_empty_nodes()
            for node in empty_nodes:
                new_state = state.clone()
                new_state.board.place_piece(node, player)
                new_state.unplaced_pieces[player] -= 1
                
                if new_state.board.forms_mill(node, player):
                    new_state.remove_mode = True
                    new_state.update_message()
                else:
                    new_state.switch_turn()
                    
                moves.append((f"place_{node}", new_state))
            return moves

        else:
            # Moving / Flying
            player_pieces = state.board.get_player_pieces(player)
            is_flying = len(player_pieces) == 3
            empty_nodes = state.board.get_all_empty_nodes()

            for p_node in player_pieces:
                valid_destinations = empty_nodes if is_flying else state.board.get_valid_moves(p_node)
                
                for dest in valid_destinations:
                    new_state = state.clone()
                    new_state.board.move_piece(p_node, dest)
                    
                    if new_state.board.forms_mill(dest, player):
                        new_state.remove_mode = True
                        new_state.update_message()
                    else:
                        new_state.switch_turn()
                        
                    moves.append((f"move_{p_node}_to_{dest}", new_state))
            return moves

    def get_best_move(self, state):
        """Returns the best next state using Minimax with Alpha-Beta pruning."""
        best_val = float('-inf')
        best_move_state = None
        
        alpha = float('-inf')
        beta = float('inf')
        
        possible_moves = self.get_all_possible_moves(state, self.ai_player)
        
        # If there are no possible moves, return None (game over will handle this)
        if not possible_moves:
            return None

        for action, next_state in possible_moves:
            # After an action, the turn might still be the AI's if they are in remove_mode.
            # So we check whose turn it is in the next state.
            is_maximizing = (next_state.turn == self.ai_player)
            
            val = self.minimax(next_state, self.max_depth - 1, alpha, beta, is_maximizing)
            
            if val > best_val:
                best_val = val
                best_move_state = next_state
                
            alpha = max(alpha, best_val)
            
        return best_move_state

    def minimax(self, state, depth, alpha, beta, is_maximizing):
        if depth == 0 or state.game_over:
            return self.evaluate(state)

        if is_maximizing:
            max_eval = float('-inf')
            possible_moves = self.get_all_possible_moves(state, self.ai_player)
            if not possible_moves:
                return self.evaluate(state)
                
            for action, next_state in possible_moves:
                still_maximizing = (next_state.turn == self.ai_player)
                eval = self.minimax(next_state, depth - 1 if not still_maximizing else depth, alpha, beta, still_maximizing)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            possible_moves = self.get_all_possible_moves(state, self.human_player)
            if not possible_moves:
                return self.evaluate(state)
                
            for action, next_state in possible_moves:
                still_minimizing = (next_state.turn == self.human_player)
                eval = self.minimax(next_state, depth - 1 if not still_minimizing else depth, alpha, beta, not still_minimizing)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
