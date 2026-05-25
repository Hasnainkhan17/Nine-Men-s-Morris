import pygame
import math
from constants import *

class UI:
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.large_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.node_positions = {}
        self.node_radius = 15
        self.piece_radius = 20

    def calculate_node_positions(self, width, height):
        """Calculates dynamic node positions based on the current window size."""
        # Top space for text, bottom space for margin
        top_margin = 100
        margin = 50
        
        # Calculate available square size
        available_height = height - top_margin - margin
        size = min(width - 2 * margin, available_height)
        
        offset_x = (width - size) / 2
        offset_y = top_margin + (available_height - size) / 2
        
        step = size / 6
        x = [offset_x + i * step for i in range(7)]
        y = [offset_y + i * step for i in range(7)]
        
        self.node_positions = {
            0: (x[0], y[0]), 1: (x[3], y[0]), 2: (x[6], y[0]),
            3: (x[1], y[1]), 4: (x[3], y[1]), 5: (x[5], y[1]),
            6: (x[2], y[2]), 7: (x[3], y[2]), 8: (x[4], y[2]),
            9: (x[0], y[3]), 10: (x[1], y[3]), 11: (x[2], y[3]),
            12: (x[4], y[3]), 13: (x[5], y[3]), 14: (x[6], y[3]),
            15: (x[2], y[4]), 16: (x[3], y[4]), 17: (x[4], y[4]),
            18: (x[1], y[5]), 19: (x[3], y[5]), 20: (x[5], y[5]),
            21: (x[0], y[6]), 22: (x[3], y[6]), 23: (x[6], y[6]),
        }

    def get_node_at_pos(self, pos):
        """Returns the node index at the given screen coordinate, or None."""
        for node, (nx, ny) in self.node_positions.items():
            dist = math.hypot(pos[0] - nx, pos[1] - ny)
            if dist < self.piece_radius + 10:
                return node
        return None

    def draw_board(self, state, selected_node):
        """Draws the entire game board, lines, and pieces."""
        self.window.fill(BG_COLOR)
        
        # Draw lines between adjacent nodes
        for node, adjacents in state.board.adjacent_nodes.items():
            start_pos = self.node_positions[node]
            for adj in adjacents:
                # To prevent drawing lines twice, only draw if adj > node
                if adj > node:
                    end_pos = self.node_positions[adj]
                    pygame.draw.line(self.window, LINE_COLOR, start_pos, end_pos, 4)
                    
        # Draw valid moves highlights if a piece is selected
        valid_moves = []
        if selected_node is not None:
            # Highlight selected piece
            pos = self.node_positions[selected_node]
            pygame.draw.circle(self.window, SELECT_COLOR, pos, self.piece_radius + 5)
            
            # Get valid moves
            is_flying = len(state.board.get_player_pieces(state.turn)) == 3
            if is_flying:
                valid_moves = state.board.get_all_empty_nodes()
            else:
                valid_moves = state.board.get_valid_moves(selected_node)
                
            # Draw valid move indicators
            for vm in valid_moves:
                vm_pos = self.node_positions[vm]
                pygame.draw.circle(self.window, HIGHLIGHT_COLOR, vm_pos, self.node_radius + 2)

        # Highlight removable opponent pieces if in remove mode
        if state.remove_mode:
            opponent = state.get_opponent()
            removable = state.board.get_removable_pieces(opponent)
            for rm in removable:
                rm_pos = self.node_positions[rm]
                pygame.draw.circle(self.window, (255, 100, 100), rm_pos, self.piece_radius + 5) # Red highlight for removal

        # Draw nodes and pieces
        for node, pos in self.node_positions.items():
            piece = state.board.get_piece(node)
            if piece == EMPTY:
                # Draw empty node point
                if node not in valid_moves: # Don't draw over highlight
                    pygame.draw.circle(self.window, NODE_COLOR, pos, self.node_radius)
            elif piece == PLAYER1:
                pygame.draw.circle(self.window, PLAYER1_COLOR, pos, self.piece_radius)
                pygame.draw.circle(self.window, PLAYER1_BORDER, pos, self.piece_radius, 2)
            elif piece == PLAYER2:
                pygame.draw.circle(self.window, PLAYER2_COLOR, pos, self.piece_radius)
                pygame.draw.circle(self.window, PLAYER2_BORDER, pos, self.piece_radius, 2)

        # Draw UI Text
        self.draw_text(state)

    def draw_text(self, state):
        """Draws the status message and unplaced pieces count."""
        # Main message
        msg_surface = self.font.render(state.message, True, TEXT_COLOR)
        msg_rect = msg_surface.get_rect(center=(self.window.get_width() / 2, 40))
        self.window.blit(msg_surface, msg_rect)
        
        # Unplaced pieces
        if state.phase == 1:
            p1_text = f"P1 Unplaced: {state.unplaced_pieces[PLAYER1]}"
            p2_text = f"P2 Unplaced: {state.unplaced_pieces[PLAYER2]}"
            
            p1_surf = self.font.render(p1_text, True, PLAYER1_COLOR)
            self.window.blit(p1_surf, (20, 20))
            
            p2_surf = self.font.render(p2_text, True, PLAYER2_BORDER) # Use border color so it's visible on light bg
            p2_rect = p2_surf.get_rect(topright=(self.window.get_width() - 20, 20))
            self.window.blit(p2_surf, p2_rect)

    def draw_main_menu(self):
        """Draws the main menu with mode selection."""
        self.window.fill(BG_COLOR)
        
        title_surf = self.large_font.render("Nine Men's Morris", True, TEXT_COLOR)
        title_rect = title_surf.get_rect(center=(self.window.get_width() / 2, 150))
        self.window.blit(title_surf, title_rect)
        
        # Create buttons
        center_x = self.window.get_width() / 2
        buttons = [
            ("Play vs Human", (center_x, 300)),
            ("Play vs AI (Easy)", (center_x, 400)),
            ("Play vs AI (Medium)", (center_x, 480)),
            ("Play vs AI (Hard)", (center_x, 560)),
        ]
        
        rects = []
        for text, center in buttons:
            surf = self.font.render(text, True, (255, 255, 255))
            rect = pygame.Rect(0, 0, 300, 60)
            rect.center = center
            pygame.draw.rect(self.window, LINE_COLOR, rect, border_radius=10)
            
            text_rect = surf.get_rect(center=center)
            self.window.blit(surf, text_rect)
            
            rects.append((rect, text))
            
        return rects
