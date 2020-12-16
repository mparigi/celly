from tabulate import tabulate

class CellAuto():
    def __init__(self, num_rows, num_cols):
        assert num_rows > 0
        assert num_cols > 0
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.grid = [[None]*self.num_cols for i in range(self.num_rows)]
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                self.grid[r][c] = self.init_cell( (r,c) )

    def init_cell(self, coordinates):
        # coordinates is a (row, column) tuple
        # should return initial state of the cell at that coordinate
        print("Abstract Method")
        assert False

    def update_cell(self, coordinates, current_state, neighbor_states):
        # coordinates is a (row, column) tuple
        # current_state is the value in that coordinate's cell
        # neighbor_states is a dictionary of the neighbors where the key is
        #   the coordinates, and the value is the value in that neighbor cell
        print("Abstract Method")
        assert False

    def get_neighbors(self, coordinates):
        r, c = coordinates
        neighbors = {}

        # get the above three and below three
        for i in range(-1, 2): # -1, 0, 1
            if r-1 >= 0 and c+i >= 0 and c+i < self.num_cols:
                neighbors[(r-1, c+i)] = self.grid[r-1][c+i]
            if r+1 < self.num_rows and c+i >= 0 and c+i < self.num_cols:
                neighbors[(r+1, c+i)] = self.grid[r+1][c+i]

        # get the sides
        if c-1 >= 0:
            neighbors[(r, c-1)] = self.grid[r][c-1]
        if c+1 < self.num_cols:
            neighbors[(r, c+1)] = self.grid[r][c+1]

        return neighbors

    def update(self):
        # call the update_cell function on each cell
        next_grid = [[None]*self.num_cols for i in range(self.num_rows)]
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                next_grid[r][c] = self.update_cell((r,c), self.grid[r][c], self.get_neighbors((r,c)))
        self.grid = next_grid


    def __str__(self):
        s = "------BEGIN------\n"
        s += tabulate(self.grid)
        s += "\n-------END-------\n"
        return s
