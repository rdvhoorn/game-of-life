import random

class GameOfLife:
    def __init__(self, grid_size: tuple[int, int]):
        self.grid_size = grid_size
        self.grid = [[0 for _ in range(grid_size[0])] for _ in range(grid_size[1])]

    def get_grid_size(self):
        return self.grid_size
    
    def get_grid(self):
        return self.grid

    def update_grid(self):
        new_grid = [[0 for _ in range(self.grid_size[0])] for _ in range(self.grid_size[1])]
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                # apply rules of game of life
                # Get current cell state
                current_state = self.grid[i][j]

                # Count alive neighbors
                alive_neighbors = self.count_live_neighbors(i, j)

                # Apply rules
                # In the new grid, all cells are dead. So we only need to check if the cell needs to be alive.

                # This happens in survival
                if current_state == 1 and (alive_neighbors == 2 or alive_neighbors == 3):
                    new_grid[i][j] = 1

                # And this happens in reproduction
                if current_state == 0 and alive_neighbors == 3:
                    new_grid[i][j] = 1

        self.grid = new_grid

    def count_live_neighbors(self, x: int, y: int):
        count = 0
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if i == x and j == y:
                    continue

                # Check if the cell is out of bounds
                if i < 0 or i >= self.grid_size[0] or j < 0 or j >= self.grid_size[1]:
                    continue

                # Count the live neighbors
                count += self.grid[i][j]
        return count
    
    def toggle_cell(self, x: int, y: int):
        self.grid[x][y] = 1 - self.grid[x][y]

    def clear_grid(self):
        self.grid = [[0 for _ in range(self.grid_size[0])] for _ in range(self.grid_size[1])]

    def set_preset(self, preset_name: str):
        self.clear_grid()
        center_x = self.grid_size[0] // 2
        center_y = self.grid_size[1] // 2

        if preset_name == "glider":
            # Glider pattern
            pattern = [
                [0, 1, 0],
                [0, 0, 1],
                [1, 1, 1]
            ]
            self._place_pattern(center_x - 1, center_y - 1, pattern)
        
        elif preset_name == "blinker":
            # Blinker pattern
            pattern = [
                [1],
                [1],
                [1]
            ]
            self._place_pattern(center_x, center_y - 1, pattern)
        
        elif preset_name == "block":
            # Block pattern
            pattern = [
                [1, 1],
                [1, 1]
            ]
            self._place_pattern(center_x - 1, center_y - 1, pattern)
        
        elif preset_name == "beehive":
            # Beehive pattern
            pattern = [
                [0, 1, 1, 0],
                [1, 0, 0, 1],
                [0, 1, 1, 0]
            ]
            self._place_pattern(center_x - 2, center_y - 1, pattern)
        
        elif preset_name == "pulsar":
            # Pulsar pattern
            pattern = [
                [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
                [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0]
            ]
            self._place_pattern(center_x - 6, center_y - 6, pattern)
        
        elif preset_name == "random":
            # Random pattern
            for i in range(self.grid_size[0]):
                for j in range(self.grid_size[1]):
                    self.grid[i][j] = random.randint(0, 1)
        
        elif preset_name == "rpentomino":
            # R-pentomino pattern
            pattern = [
                [0, 1, 1],
                [1, 1, 0],
                [0, 1, 0]
            ]
            self._place_pattern(center_x - 1, center_y - 1, pattern)
        
        elif preset_name == "diehard":
            # Diehard pattern
            pattern = [
                [0, 0, 0, 0, 0, 0, 1, 0],
                [1, 1, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 1, 1, 1]
            ]
            self._place_pattern(center_x - 4, center_y - 1, pattern)
        
        elif preset_name == "acorn":
            # Acorn pattern
            pattern = [
                [0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [1, 1, 0, 0, 1, 1, 1]
            ]
            self._place_pattern(center_x - 3, center_y - 1, pattern)

    def _place_pattern(self, start_x: int, start_y: int, pattern: list[list[int]]):
        for i in range(len(pattern)):
            for j in range(len(pattern[0])):
                if 0 <= start_x + i < self.grid_size[0] and 0 <= start_y + j < self.grid_size[1]:
                    self.grid[start_x + i][start_y + j] = pattern[i][j]
