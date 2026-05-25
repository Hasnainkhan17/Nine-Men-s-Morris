from constants import EMPTY

class Board:
    """
    Represents the Nine Men's Morris board.
    There are 24 nodes/intersections on the board.
    Nodes are indexed 0 to 23.
    """
    def __init__(self):
        # 0 means empty, 1 means Player 1, 2 means Player 2
        self.state = [EMPTY] * 24
        
        # Adjacency list defining which nodes are connected
        self.adjacent_nodes = {
            0: [1, 9],
            1: [0, 2, 4],
            2: [1, 14],
            3: [4, 10],
            4: [1, 3, 5, 7],
            5: [4, 13],
            6: [7, 11],
            7: [4, 6, 8],
            8: [7, 12],
            9: [0, 10, 21],
            10: [3, 9, 11, 18],
            11: [6, 10, 15],
            12: [8, 13, 17],
            13: [5, 12, 14, 20],
            14: [2, 13, 23],
            15: [11, 16],
            16: [15, 17, 19],
            17: [12, 16],
            18: [10, 19],
            19: [16, 18, 20, 22],
            20: [13, 19],
            21: [9, 22],
            22: [19, 21, 23],
            23: [14, 22]
        }
        
        # All possible mills (3-in-a-row)
        self.mills = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),       # Top horizontals
            (9, 10, 11), (12, 13, 14),             # Middle horizontals
            (15, 16, 17), (18, 19, 20), (21, 22, 23), # Bottom horizontals
            (0, 9, 21), (3, 10, 18), (6, 11, 15),  # Left verticals
            (1, 4, 7), (16, 19, 22),               # Middle verticals
            (8, 12, 17), (5, 13, 20), (2, 14, 23)  # Right verticals
        ]

    def clone(self):
        """Returns a deep copy of the board."""
        new_board = Board()
        new_board.state = self.state[:]
        return new_board

    def is_empty(self, node):
        """Check if a node is empty."""
        return self.state[node] == EMPTY

    def get_piece(self, node):
        """Get the player occupying the node."""
        return self.state[node]

    def place_piece(self, node, player):
        """Place a piece on the board."""
        self.state[node] = player

    def move_piece(self, from_node, to_node):
        """Move a piece from one node to another."""
        self.state[to_node] = self.state[from_node]
        self.state[from_node] = EMPTY

    def remove_piece(self, node):
        """Remove a piece from the board."""
        self.state[node] = EMPTY

    def is_adjacent(self, node1, node2):
        """Check if two nodes are connected by a line."""
        return node2 in self.adjacent_nodes[node1]

    def get_valid_moves(self, node):
        """Return a list of empty adjacent nodes for a given node."""
        return [n for n in self.adjacent_nodes[node] if self.is_empty(n)]

    def get_all_empty_nodes(self):
        """Return a list of all empty nodes (useful for flying phase)."""
        return [i for i, piece in enumerate(self.state) if piece == EMPTY]

    def get_player_pieces(self, player):
        """Return a list of nodes occupied by a specific player."""
        return [i for i, piece in enumerate(self.state) if piece == player]

    def forms_mill(self, node, player):
        """
        Check if placing/moving a piece to 'node' forms a mill for 'player'.
        """
        for mill in self.mills:
            if node in mill:
                if all(self.state[n] == player or n == node for n in mill):
                    return True
        return False

    def is_part_of_mill(self, node, player):
        """
        Check if a given piece is currently part of a mill.
        """
        if self.state[node] != player:
            return False
            
        for mill in self.mills:
            if node in mill:
                if all(self.state[n] == player for n in mill):
                    return True
        return False

    def get_removable_pieces(self, player):
        """
        Return a list of pieces belonging to 'player' that can be removed.
        A piece can be removed if it's NOT part of a mill.
        However, if ALL pieces are part of a mill, then any piece can be removed.
        """
        pieces = self.get_player_pieces(player)
        non_mill_pieces = [p for p in pieces if not self.is_part_of_mill(p, player)]
        
        if non_mill_pieces:
            return non_mill_pieces
        return pieces # All pieces in mills, so any can be removed
