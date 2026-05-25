from constants import PLAYER1, PLAYER2, EMPTY
from board import Board

# Game Phases
PHASE_PLACING = 1
PHASE_MOVING_FLYING = 2

class GameState:
    """Manages the overall game state, rules, turns, and phase transitions."""
    def __init__(self):
        self.board = Board()
        self.turn = PLAYER1
        
        # Each player starts with 9 unplaced pieces
        self.unplaced_pieces = {PLAYER1: 9, PLAYER2: 9}
        
        # Phase tracking
        self.phase = PHASE_PLACING
        
        # When True, the current player must select an opponent piece to remove
        self.remove_mode = False
        
        self.game_over = False
        self.winner = None
        self.message = "Player 1's Turn (Placing)"

    def clone(self):
        """Returns a deep copy of the game state."""
        new_state = GameState()
        new_state.board = self.board.clone()
        new_state.turn = self.turn
        new_state.unplaced_pieces = self.unplaced_pieces.copy()
        new_state.phase = self.phase
        new_state.remove_mode = self.remove_mode
        new_state.game_over = self.game_over
        new_state.winner = self.winner
        new_state.message = self.message
        return new_state

    def switch_turn(self):
        """Switches the turn to the other player and updates the phase if necessary."""
        self.turn = PLAYER2 if self.turn == PLAYER1 else PLAYER1
        self.update_phase()
        self.update_message()
        self.check_game_over()

    def get_opponent(self):
        return PLAYER2 if self.turn == PLAYER1 else PLAYER1

    def update_phase(self):
        """Updates the game phase based on unplaced pieces."""
        if self.unplaced_pieces[PLAYER1] == 0 and self.unplaced_pieces[PLAYER2] == 0:
            self.phase = PHASE_MOVING_FLYING

    def update_message(self):
        """Updates the status message for the UI."""
        if self.game_over:
            winner_name = "Player 1" if self.winner == PLAYER1 else "Player 2"
            self.message = f"Game Over! {winner_name} Wins!"
            return

        player_name = "Player 1" if self.turn == PLAYER1 else "Player 2"
        if self.remove_mode:
            self.message = f"{player_name} formed a Mill! Remove an opponent's piece."
        elif self.phase == PHASE_PLACING:
            self.message = f"{player_name}'s Turn (Placing - {self.unplaced_pieces[self.turn]} left)"
        else:
            pieces_left = len(self.board.get_player_pieces(self.turn))
            if pieces_left == 3:
                self.message = f"{player_name}'s Turn (Flying Mode!)"
            else:
                self.message = f"{player_name}'s Turn (Moving)"

    def handle_click(self, node, selected_node):
        """
        Handles a node click based on the current phase and state.
        Returns the new selected_node (if any).
        """
        if self.game_over:
            return None

        # Handle Remove Mode
        if self.remove_mode:
            opponent = self.get_opponent()
            if self.board.get_piece(node) == opponent:
                removable = self.board.get_removable_pieces(opponent)
                if node in removable:
                    self.board.remove_piece(node)
                    self.remove_mode = False
                    self.switch_turn()
            return None

        # Handle Placing Phase
        if self.phase == PHASE_PLACING:
            if self.board.is_empty(node):
                self.board.place_piece(node, self.turn)
                self.unplaced_pieces[self.turn] -= 1
                
                if self.board.forms_mill(node, self.turn):
                    self.remove_mode = True
                    self.update_message()
                else:
                    self.switch_turn()
            return None

        # Handle Moving/Flying Phase
        if self.phase == PHASE_MOVING_FLYING:
            # Select a piece
            if self.board.get_piece(node) == self.turn:
                return node
            
            # Move selected piece
            if selected_node is not None and self.board.is_empty(node):
                player_pieces = len(self.board.get_player_pieces(self.turn))
                
                # Check if valid move (Flying allows any empty node, Moving requires adjacency)
                if player_pieces == 3 or self.board.is_adjacent(selected_node, node):
                    self.board.move_piece(selected_node, node)
                    
                    if self.board.forms_mill(node, self.turn):
                        self.remove_mode = True
                        self.update_message()
                    else:
                        self.switch_turn()
                    return None
                    
            return selected_node
        
        return None

    def check_game_over(self):
        """Checks if the game has been won by the current player's opponent."""
        if self.phase == PHASE_PLACING:
            return False
            
        # Player loses if they have less than 3 pieces
        p1_pieces = len(self.board.get_player_pieces(PLAYER1))
        p2_pieces = len(self.board.get_player_pieces(PLAYER2))
        
        if p1_pieces < 3:
            self.game_over = True
            self.winner = PLAYER2
            self.update_message()
            return True
        elif p2_pieces < 3:
            self.game_over = True
            self.winner = PLAYER1
            self.update_message()
            return True
            
        # Player loses if they have no valid moves (and they are not flying)
        current_player_pieces = self.board.get_player_pieces(self.turn)
        if len(current_player_pieces) > 3:
            has_moves = False
            for piece_node in current_player_pieces:
                if len(self.board.get_valid_moves(piece_node)) > 0:
                    has_moves = True
                    break
            
            if not has_moves:
                self.game_over = True
                self.winner = self.get_opponent()
                self.update_message()
                return True
                
        return False
