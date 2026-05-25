import pygame
import sys
from constants import *
from game import GameState
from ui import UI
from ai import MinimaxAI

def main():
    pygame.init()
    
    # Enable resizing
    window = pygame.display.set_mode((INITIAL_WIDTH, INITIAL_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Nine Men's Morris - AI Project")
    
    clock = pygame.time.Clock()
    ui = UI(window)
    ui.calculate_node_positions(INITIAL_WIDTH, INITIAL_HEIGHT)
    
    # State flags
    in_menu = True
    ai_enabled = False
    ai = None
    
    state = None
    selected_node = None

    while True:
        # Check if it is AI's turn
        if not in_menu and ai_enabled and not state.game_over:
            # AI always plays as PLAYER2 in our setup (or whoever it was configured as)
            if state.turn == ai.ai_player:
                best_next_state = ai.get_best_move(state)
                if best_next_state is not None:
                    # Update game state to the AI's chosen state
                    state = best_next_state
                    selected_node = None
                else:
                    # If AI has no moves, check game over
                    state.check_game_over()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.VIDEORESIZE:
                # Handle window resizing
                window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                ui.calculate_node_positions(event.w, event.h)
                
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                
                if in_menu:
                    # Handle menu clicks
                    buttons = ui.draw_main_menu()
                    for rect, text in buttons:
                        if rect.collidepoint(pos):
                            in_menu = False
                            state = GameState()
                            selected_node = None
                            
                            if "Human" in text:
                                ai_enabled = False
                            else:
                                ai_enabled = True
                                if "Easy" in text:
                                    ai = MinimaxAI(ai_player=PLAYER2, difficulty='easy')
                                elif "Medium" in text:
                                    ai = MinimaxAI(ai_player=PLAYER2, difficulty='medium')
                                elif "Hard" in text:
                                    ai = MinimaxAI(ai_player=PLAYER2, difficulty='hard')
                else:
                    # Handle game board clicks
                    if state.game_over:
                        # Click anywhere to return to menu
                        in_menu = True
                        continue
                        
                    # Ignore click if it's AI's turn
                    if ai_enabled and state.turn == ai.ai_player:
                        continue
                        
                    clicked_node = ui.get_node_at_pos(pos)
                    
                    if clicked_node is not None:
                        # Process move
                        new_selected = state.handle_click(clicked_node, selected_node)
                        selected_node = new_selected

        # Rendering
        if in_menu:
            ui.draw_main_menu()
        else:
            ui.draw_board(state, selected_node)
            
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
