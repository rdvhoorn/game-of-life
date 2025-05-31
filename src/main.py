import pygame
import sys
import random

from src.game_of_life import GameOfLife

# --- Constants ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SIDEBAR_WIDTH = 200
GRID_COLS = 100
GRID_ROWS = 100

# FPS
SIDEBAR_FPS = 30
GAME_FPS = 3

# Colors
COLOR_BG = (0, 0, 0)
COLOR_SIDEBAR = (150, 150, 150)
COLOR_PLAY_BUTTON = (200, 200, 200)
COLOR_PLAY_BUTTON_HOVER = (220, 220, 220)
COLOR_TEXT = (0, 0, 0)
COLOR_BORDER = (100, 100, 100)
COLOR_GRID_ON = (178, 34, 34)
COLOR_GRID_OFF = (107, 142, 35)

# --- Init ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Side Menu with Independent FPS")
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# --- State ---
paused = True
GAME_SQUARE_WIDTH = (SCREEN_WIDTH - SIDEBAR_WIDTH) / GRID_COLS
GAME_SQUARE_HEIGHT = SCREEN_HEIGHT / GRID_ROWS

game_rects = [[None for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

for row in range(GRID_ROWS):
    for col in range(GRID_COLS):
        x = SIDEBAR_WIDTH + col * GAME_SQUARE_WIDTH
        y = row * GAME_SQUARE_HEIGHT
        game_rects[row][col] = pygame.Rect(x, y, GAME_SQUARE_WIDTH, GAME_SQUARE_HEIGHT)

button_rect = pygame.Rect(25, 50, 150, 50)

# Timers
last_game_update = 0
game_update_interval = 1000 // GAME_FPS

# --- Functions ---
def draw_button(text, rect, hovered):
    color = COLOR_PLAY_BUTTON_HOVER if hovered else COLOR_PLAY_BUTTON
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, COLOR_BORDER, rect, 3)
    label = font.render(text, True, COLOR_TEXT)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

def draw_sidebar(mouse_pos):
    pygame.draw.rect(screen, COLOR_SIDEBAR, (0, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT))
    is_hovered = button_rect.collidepoint(mouse_pos)
    button_text = "Play" if paused else "Pause"
    draw_button(button_text, button_rect, is_hovered)

def draw_game_grid(game_of_life: GameOfLife):
    grid_state = game_of_life.get_grid()

    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            color = COLOR_GRID_ON if grid_state[row][col] else COLOR_GRID_OFF
            pygame.draw.rect(screen, color, game_rects[row][col], 1)

def update_game_state(game_of_life: GameOfLife):
    game_of_life.update_grid()

def handle_events(game_of_life: GameOfLife):
    global paused
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                paused = not paused

            # If the user clicks on a cell, toggle the cell's state
            if event.button == 1:
                x, y = event.pos
                if x >= SIDEBAR_WIDTH and x <= SCREEN_WIDTH - SIDEBAR_WIDTH:
                    col = (x - SIDEBAR_WIDTH) // GAME_SQUARE_WIDTH
                    row = y // GAME_SQUARE_HEIGHT
                    game_of_life.toggle_cell(int(row), int(col))


def main(game_of_life: GameOfLife):
    global last_game_update
    while True:
        now = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(COLOR_BG)

        handle_events(game_of_life)
        draw_sidebar(mouse_pos)
        draw_game_grid(game_of_life)

        # Update game at GAME_FPS
        if not paused and now - last_game_update > game_update_interval:
            update_game_state(game_of_life)
            last_game_update = now

        pygame.display.flip()
        clock.tick(SIDEBAR_FPS)

# --- Entry Point ---
if __name__ == "__main__":
    game_of_life_object = GameOfLife((GRID_COLS, GRID_ROWS))
    main(game_of_life_object)
