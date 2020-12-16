from cellauto import CellAuto

class GameOfLife(CellAuto):
    def __init__(self, num_rows, num_cols, initial_live_cells):
        # check that all initial live cells are actually within range
        for r,c in initial_live_cells:
            assert r >=0 and r < num_rows and c >=0 and c < num_cols

        self.initial_live_cells = initial_live_cells
        super().__init__(num_rows, num_cols)
    
    def init_cell(self, coordinates):
        return coordinates in self.initial_live_cells

    def update_cell(self, coordinates, current_state, neighbor_states):
        # if a cell is alive, it stays alive if it has 2 or 3 alive neighbors
        # if a cell is dead, it comes back to life if it has 3 alive neighbors
        num_neighbors = len([el for el in neighbor_states.values() if el])
        if current_state:
            return num_neighbors == 2 or num_neighbors == 3
        else:
            return num_neighbors == 3