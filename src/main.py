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
GAME_FPS = 50
MIN_FPS = 1
MAX_FPS = 50

# Colors
COLOR_BG = (0, 0, 0)
COLOR_SIDEBAR = (150, 150, 150)
COLOR_PLAY_BUTTON = (200, 200, 200)
COLOR_PLAY_BUTTON_HOVER = (220, 220, 220)
COLOR_TEXT = (0, 0, 0)
COLOR_BORDER = (100, 100, 100)
COLOR_GRID_ON = (178, 34, 34)
COLOR_GRID_OFF = (107, 142, 35)
COLOR_SLIDER = (100, 100, 100)
COLOR_SLIDER_HOVER = (120, 120, 120)

# Preset patterns
PRESETS = [
    "glider", "blinker", "block",
    "beehive", "pulsar", "random",
    "rpentomino", "diehard", "acorn"
]

# --- Init ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Side Menu with Independent FPS")
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)
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

# Button and slider rectangles
button_rect = pygame.Rect(25, 50, 150, 50)
slider_rect = pygame.Rect(25, 150, 150, 20)
slider_knob_rect = pygame.Rect(0, 0, 20, 30)
slider_dragging = False

# Preset buttons
preset_button_size = 50
preset_button_spacing = 10
preset_buttons = []
start_y = 200
for i, preset in enumerate(PRESETS):
    row = i // 3
    col = i % 3
    x = 25 + col * (preset_button_size + preset_button_spacing)
    y = start_y + row * (preset_button_size + preset_button_spacing)
    preset_buttons.append({
        'rect': pygame.Rect(x, y, preset_button_size, preset_button_size),
        'name': preset
    })

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

def draw_slider(rect, knob_rect, value, dragging):
    # Draw slider track
    pygame.draw.rect(screen, COLOR_SLIDER, rect)
    pygame.draw.rect(screen, COLOR_BORDER, rect, 1)
    
    # Draw knob
    knob_color = COLOR_SLIDER_HOVER if dragging else COLOR_SLIDER
    pygame.draw.rect(screen, knob_color, knob_rect)
    pygame.draw.rect(screen, COLOR_BORDER, knob_rect, 1)
    
    # Draw value text
    value_text = small_font.render(f"FPS: {value}", True, COLOR_TEXT)
    screen.blit(value_text, (rect.x, rect.y - 25))

def update_slider_value(mouse_x):
    global GAME_FPS, game_update_interval
    # Calculate new value based on mouse position
    relative_x = max(0, min(mouse_x - slider_rect.x, slider_rect.width))
    GAME_FPS = MIN_FPS + int((relative_x / slider_rect.width) * (MAX_FPS - MIN_FPS))
    game_update_interval = 1000 // GAME_FPS

def draw_sidebar(mouse_pos):
    pygame.draw.rect(screen, COLOR_SIDEBAR, (0, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT))
    
    # Draw play/pause button
    is_hovered = button_rect.collidepoint(mouse_pos)
    button_text = "Play" if paused else "Pause"
    draw_button(button_text, button_rect, is_hovered)
    
    # Draw FPS slider
    relative_x = ((GAME_FPS - MIN_FPS) / (MAX_FPS - MIN_FPS)) * slider_rect.width
    slider_knob_rect.centerx = slider_rect.x + relative_x
    slider_knob_rect.centery = slider_rect.centery
    draw_slider(slider_rect, slider_knob_rect, GAME_FPS, slider_dragging)
    
    # Draw preset buttons
    for button in preset_buttons:
        is_hovered = button['rect'].collidepoint(mouse_pos)
        color = COLOR_PLAY_BUTTON_HOVER if is_hovered else COLOR_PLAY_BUTTON
        pygame.draw.rect(screen, color, button['rect'])
        pygame.draw.rect(screen, COLOR_BORDER, button['rect'], 2)
        
        # Draw preset name
        text = small_font.render(button['name'], True, COLOR_TEXT)
        text_rect = text.get_rect(center=button['rect'].center)
        screen.blit(text, text_rect)

def draw_game_grid(game_of_life: GameOfLife):
    grid_state = game_of_life.get_grid()

    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            color = COLOR_GRID_ON if grid_state[row][col] else COLOR_GRID_OFF
            pygame.draw.rect(screen, color, game_rects[row][col])
            pygame.draw.rect(screen, (0, 0, 0), game_rects[row][col], width=1)

def update_game_state(game_of_life: GameOfLife):
    game_of_life.update_grid()

def handle_events(game_of_life: GameOfLife):
    global paused, slider_dragging
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                paused = not paused
            elif slider_knob_rect.collidepoint(event.pos):
                slider_dragging = True
            else:
                # Check preset buttons
                for button in preset_buttons:
                    if button['rect'].collidepoint(event.pos):
                        game_of_life.set_preset(button['name'])
                        paused = True  # Pause the game when setting a new pattern

            # If the user clicks on a cell, toggle the cell's state
            if event.button == 1:
                x, y = event.pos
                if x >= SIDEBAR_WIDTH and x <= SCREEN_WIDTH - SIDEBAR_WIDTH:
                    col = (x - SIDEBAR_WIDTH) // GAME_SQUARE_WIDTH
                    row = y // GAME_SQUARE_HEIGHT
                    game_of_life.toggle_cell(int(row), int(col))
        
        elif event.type == pygame.MOUSEBUTTONUP:
            slider_dragging = False
        
        elif event.type == pygame.MOUSEMOTION and slider_dragging:
            update_slider_value(event.pos[0])

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
