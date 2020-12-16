from cellauto import CellAuto
from math import ceil

def mean(l):
    return sum(l) / len(l)

def clip(val, lim):
    if abs(val) > lim:
        return lim
    return val

class LunchTable(CellAuto):
    def __init__(self, num_rows, num_cols):
        super().__init__(num_rows, num_cols)
    
    def init_cell(self, coordinates):
        # each cell is a (money, happiness, hunger) tuple
        return (0, 0, 0)

    def update_cell(self, coordinates, current_state, neighbor_states):
        money, happiness, hunger = current_state

        average_neighbor_hunger = mean([s[2] for s in neighbor_states.values()])
        if average_neighbor_hunger > hunger:
            new_money = money - 1
        else:
            new_money = money + 1

        new_happiness = money + hunger - ceil(average_neighbor_hunger)

        neighbor_happy_count = len([s[1] for s in neighbor_states.values() if s[1] > 0])
        new_hunger = clip(neighbor_happy_count - money, 10)


        return (new_money, new_happiness, new_hunger)

        