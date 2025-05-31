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
