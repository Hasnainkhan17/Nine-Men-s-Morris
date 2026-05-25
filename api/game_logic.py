# game_logic.py
import math

# Constants
EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2
PHASE_PLACING = 1
PHASE_MOVING_FLYING = 2

class Board:
    def __init__(self):
        self.state = [EMPTY] * 24
        self.adjacent_nodes = {
            0: [1, 9], 1: [0, 2, 4], 2: [1, 14], 3: [4, 10], 4: [1, 3, 5, 7], 5: [4, 13],
            6: [7, 11], 7: [4, 6, 8], 8: [7, 12], 9: [0, 10, 21], 10: [3, 9, 11, 18],
            11: [6, 10, 15], 12: [8, 13, 17], 13: [5, 12, 14, 20], 14: [2, 13, 23],
            15: [11, 16], 16: [15, 17, 19], 17: [12, 16], 18: [10, 19], 19: [16, 18, 20, 22],
            20: [13, 19], 21: [9, 22], 22: [19, 21, 23], 23: [14, 22]
        }
        self.mills = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11), (12, 13, 14),
            (15, 16, 17), (18, 19, 20), (21, 22, 23), (0, 9, 21), (3, 10, 18),
            (6, 11, 15), (1, 4, 7), (16, 19, 22), (8, 12, 17), (5, 13, 20), (2, 14, 23)
        ]

    def clone(self):
        new_board = Board()
        new_board.state = self.state[:]
        return new_board

    def is_empty(self, node): return self.state[node] == EMPTY
    def get_piece(self, node): return self.state[node]
    def place_piece(self, node, player): self.state[node] = player
    def move_piece(self, from_node, to_node):
        self.state[to_node] = self.state[from_node]
        self.state[from_node] = EMPTY
    def remove_piece(self, node): self.state[node] = EMPTY
    def is_adjacent(self, node1, node2): return node2 in self.adjacent_nodes[node1]
    def get_valid_moves(self, node): return [n for n in self.adjacent_nodes[node] if self.is_empty(n)]
    def get_all_empty_nodes(self): return [i for i, p in enumerate(self.state) if p == EMPTY]
    def get_player_pieces(self, player): return [i for i, p in enumerate(self.state) if p == player]

    def forms_mill(self, node, player):
        for mill in self.mills:
            if node in mill:
                if all(self.state[n] == player or n == node for n in mill):
                    return True
        return False

    def is_part_of_mill(self, node, player):
        if self.state[node] != player: return False
        for mill in self.mills:
            if node in mill:
                if all(self.state[n] == player for n in mill):
                    return True
        return False

    def get_removable_pieces(self, player):
        pieces = self.get_player_pieces(player)
        non_mill = [p for p in pieces if not self.is_part_of_mill(p, player)]
        return non_mill if non_mill else pieces

class GameState:
    def __init__(self):
        self.board = Board()
        self.turn = PLAYER1
        self.unplaced_pieces = {PLAYER1: 9, PLAYER2: 9}
        self.phase = PHASE_PLACING
        self.remove_mode = False
        self.game_over = False
        self.winner = None

    def clone(self):
        new_state = GameState()
        new_state.board = self.board.clone()
        new_state.turn = self.turn
        new_state.unplaced_pieces = self.unplaced_pieces.copy()
        new_state.phase = self.phase
        new_state.remove_mode = self.remove_mode
        new_state.game_over = self.game_over
        new_state.winner = self.winner
        return new_state

    def switch_turn(self):
        self.turn = PLAYER2 if self.turn == PLAYER1 else PLAYER1
        if self.unplaced_pieces[PLAYER1] == 0 and self.unplaced_pieces[PLAYER2] == 0:
            self.phase = PHASE_MOVING_FLYING
        self.check_game_over()

    def check_game_over(self):
        if self.phase == PHASE_PLACING: return False
        p1 = len(self.board.get_player_pieces(PLAYER1))
        p2 = len(self.board.get_player_pieces(PLAYER2))
        
        if p1 < 3: self.game_over, self.winner = True, PLAYER2; return True
        if p2 < 3: self.game_over, self.winner = True, PLAYER1; return True
        
        curr_pieces = self.board.get_player_pieces(self.turn)
        if len(curr_pieces) > 3:
            if not any(len(self.board.get_valid_moves(n)) > 0 for n in curr_pieces):
                self.game_over, self.winner = True, (PLAYER2 if self.turn == PLAYER1 else PLAYER1)
                return True
        return False

    def to_dict(self):
        return {
            "board": self.board.state,
            "turn": self.turn,
            "unplaced_pieces": self.unplaced_pieces,
            "phase": self.phase,
            "remove_mode": self.remove_mode,
            "game_over": self.game_over,
            "winner": self.winner
        }

    @staticmethod
    def from_dict(data):
        state = GameState()
        state.board.state = data["board"]
        state.turn = data["turn"]
        state.unplaced_pieces = {int(k): v for k, v in data["unplaced_pieces"].items()}
        state.phase = data["phase"]
        state.remove_mode = data["remove_mode"]
        state.game_over = data["game_over"]
        state.winner = data.get("winner")
        return state

class MinimaxAI:
    def __init__(self, ai_player=PLAYER2, difficulty='medium'):
        self.ai_player = ai_player
        self.human_player = PLAYER1 if ai_player == PLAYER2 else PLAYER2
        self.max_depth = 2 if difficulty == 'easy' else (4 if difficulty == 'hard' else 3)

    def evaluate(self, state):
        if state.game_over:
            return float('inf') if state.winner == self.ai_player else float('-inf')
        ai_pieces = len(state.board.get_player_pieces(self.ai_player))
        human_pieces = len(state.board.get_player_pieces(self.human_player))
        return (ai_pieces - human_pieces) * 10

    def get_all_possible_moves(self, state, player):
        moves = []
        if state.remove_mode:
            opponent = PLAYER2 if player == PLAYER1 else PLAYER1
            for r_node in state.board.get_removable_pieces(opponent):
                new_state = state.clone()
                new_state.board.remove_piece(r_node)
                new_state.remove_mode = False
                new_state.switch_turn()
                moves.append(new_state)
            return moves

        if state.phase == PHASE_PLACING:
            for node in state.board.get_all_empty_nodes():
                new_state = state.clone()
                new_state.board.place_piece(node, player)
                new_state.unplaced_pieces[player] -= 1
                if new_state.board.forms_mill(node, player): new_state.remove_mode = True
                else: new_state.switch_turn()
                moves.append(new_state)
            return moves
        else:
            pieces = state.board.get_player_pieces(player)
            is_flying = len(pieces) == 3
            empty_nodes = state.board.get_all_empty_nodes()
            for p_node in pieces:
                dests = empty_nodes if is_flying else state.board.get_valid_moves(p_node)
                for dest in dests:
                    new_state = state.clone()
                    new_state.board.move_piece(p_node, dest)
                    if new_state.board.forms_mill(dest, player): new_state.remove_mode = True
                    else: new_state.switch_turn()
                    moves.append(new_state)
            return moves

    def get_best_move(self, state):
        best_val, best_state = float('-inf'), None
        alpha, beta = float('-inf'), float('inf')
        moves = self.get_all_possible_moves(state, self.ai_player)
        if not moves: return None

        for next_state in moves:
            is_max = (next_state.turn == self.ai_player)
            val = self.minimax(next_state, self.max_depth - 1, alpha, beta, is_max)
            if val > best_val: best_val, best_state = val, next_state
            alpha = max(alpha, best_val)
        return best_state

    def minimax(self, state, depth, alpha, beta, is_maximizing):
        if depth == 0 or state.game_over: return self.evaluate(state)
        
        player = self.ai_player if is_maximizing else self.human_player
        moves = self.get_all_possible_moves(state, player)
        if not moves: return self.evaluate(state)

        if is_maximizing:
            max_eval = float('-inf')
            for next_state in moves:
                still_max = (next_state.turn == self.ai_player)
                eval = self.minimax(next_state, depth - 1 if not still_max else depth, alpha, beta, still_max)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha: break
            return max_eval
        else:
            min_eval = float('inf')
            for next_state in moves:
                still_min = (next_state.turn == self.human_player)
                eval = self.minimax(next_state, depth - 1 if not still_min else depth, alpha, beta, not still_min)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha: break
            return min_eval
