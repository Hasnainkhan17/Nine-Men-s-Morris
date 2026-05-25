import pygame

# Colors (Minimalist theme)
BG_COLOR = (250, 250, 250)      # Very light off-white background
LINE_COLOR = (40, 40, 40)       # Dark gray for board lines
NODE_COLOR = (200, 200, 200)    # Light gray for empty intersection points
HIGHLIGHT_COLOR = (120, 220, 120) # Soft green for valid moves
SELECT_COLOR = (100, 180, 255)  # Soft blue for selected piece
TEXT_COLOR = (30, 30, 30)       # Dark text
PLAYER1_COLOR = (20, 20, 20)    # Black pieces
PLAYER1_BORDER = (0, 0, 0)      # Black piece border
PLAYER2_COLOR = (245, 245, 245) # White pieces
PLAYER2_BORDER = (150, 150, 150) # Gray border for white pieces so they show on bg

# Window Settings
INITIAL_WIDTH = 800
INITIAL_HEIGHT = 800
FPS = 60

# Game Logic Constants
EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2
