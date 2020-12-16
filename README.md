# celly
A simple cellular automata library in vanilla Python.


## Setup
Written for Python3. Install the requirements with `pip install -r requirements.txt`. To quickly test it out, run the `test_run.py` file like `python test_run.py`.
## Walkthrough

We start with an abstract base class, `CellAuto` in `cellauto.py`.

`CellAuto` does a few things. For initialization, it takes in two numbers: the number of rows and the number of columns. It then creates a grid of that size, and calls the `init_cell` function to initialize each cell. 

The `init_cell` function must be overridden by a subclass. Given the coordinates of the cell, `init_cell` should return the value of the state initially at that point. The type of variable used for this may vary depending on the kind of automata you are building.

To update the state of the grid, i.e. take a step of time, the `update` function calls the `update_cell` function on each cell of the grid. `update_cell`, similar to `init_cell` must be overridden by a subclass. Given the coordinates of a cell, the current value in that cell, and a dictionary of the values of its neighboring cells, `update_cell` should return the new value of the cell.

The neighbors of a cell are its 8 natural neighbors, i.e. left, right, up, down, and the four diagonals. Edges are simply cut off; cells at the edge may have less than 8 neighbors. The format of the neighbors dictionary given to `update_cell` is as follows: the keys are `(r,c)` tuples of the row and column of the neighbor, and the values are the corresponding value in that neighbor cell.

Finally, the `__str__` method is implemented, so you can print an instance of this class like `print(ca)`. We use the `tabulate` library so it's pretty!

## Example: Game of Life

To illustrate how to use this library, we show the canonical example of [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).

The implementation in `game_of_life.py` is so short, we'll reproduce it here (sans headers and comments):

```python
class GameOfLife(CellAuto):
    def __init__(self, num_rows, num_cols, initial_live_cells):
        for r,c in initial_live_cells:
            assert r >=0 and r < num_rows and c >=0 and c < num_cols
        self.initial_live_cells = initial_live_cells
        super().__init__(num_rows, num_cols)
    
    def init_cell(self, coordinates):
        return coordinates in self.initial_live_cells

    def update_cell(self, coordinates, current_state, neighbor_states):
        num_neighbors = len([el for el in neighbor_states.values() if el])
        if current_state:
            return num_neighbors == 2 or num_neighbors == 3
        else:
            return num_neighbors == 3
```

We want the game to take in an additional parameter in initialization: a list of the coordinates that are initially alive. To do this, we override the `__init__` function and give the additional parameter. First we check to make sure all the initially alive coordinates given are actually valid within the range of the grid. Then we save this list and call the base class' `__init__` to handle the normal initialization process.

We will use a boolean value as the state of each cell - True indicating alive and False indicating dead.

When we override the `init_cell` function, we return True if the coordinates are in the initially alive list, and False otherwise.

To update a cell, we count how many of its neighbors are alive. Following the Game of Life update rule, if a cell is alive, it stays alive if it has exactly 2 or 3 alive neighbors. If a cell is dead, it comes to life if it has exactly 3 alive neighbors.

That's it! To run it, we can do something like the following:

```python
life = GameOfLife(10, 10, [(0,0), (5,5), (5,6), (6,5), (6,6), (6,7)])
for i in range(15):
    print(life)
    life.update()
```

This will print out 15 steps of the Game of Life with the according initial conditions.

## Example: Getting Complex Behavior with Lunch Table

I made up a cellular automata that does the following.

Each cell is a kid eating lunch at the big school cafeteria. They each have three properties: money, happiness, and hunger. These are all represented with numbers. Every iteration, the following update happens:

 - You like to feed your friends. If the average hunger of the neighbors is more than your hunger, you lose 1 money. Otherwise you gain 1 money.
  - Money makes you happy, but you also like to be a bit hungrier than your friends (ambition is good). Your new happiness is your money plus your hunger minus the average hunger of your neighbors (ceiling'd).
 - If everyone around you is happy, it makes you hungry... but money buys you food. Your new hunger level is the number of neighbors that have positive happiness levels minus the amount of money you have. This is capped at -10 and +10; [kids shouldn't be going into lunch debt](https://foodrevolution.org/blog/school-lunch-debt/).


This logic is implemented in `lunch_table.py`. The initial state is set to where all kids start with zero money, zero happiness, and zero hunger. Tabula rasa, amirite. But we'll see what happens when we mess with this.

If you run the simulation for 100 steps, you get a grid state like
```
---------  ---------  ---------  ---------  ---------
(1, 4, 3)  (3, 1, 1)  (3, 5, 3)  (3, 1, 1)  (1, 4, 3)
(3, 1, 1)  (5, 3, 2)  (7, 7, 2)  (5, 3, 2)  (3, 1, 1)
(3, 5, 3)  (7, 7, 2)  (7, 7, 2)  (7, 7, 2)  (3, 5, 3)
(3, 1, 1)  (5, 3, 2)  (7, 7, 2)  (5, 3, 2)  (3, 1, 1)
(1, 4, 3)  (3, 1, 1)  (3, 5, 3)  (3, 1, 1)  (1, 4, 3)
---------  ---------  ---------  ---------  ---------
```
_Note: each state is (money, happiness, hunger)_

...but this isn't a steady state. I'm not **certain** if this converges to anything very far down the line, but I'm pretty certain it oscillates between 6 states. Try it for yourself!

Now lets tweak the initial conditions so everyone starts with an initial state of `(0, 0.001, 0)`. I get an oscillation of 6 entirely different states! This [sensitivity to initial conditions](https://en.wikipedia.org/wiki/Butterfly_effect) is a hallmark of weird nonlinear dynamical systems like this.

I honestly have no idea about much of the dynamics of this system - I made it up. But I'm sure there's some interesting things to be found.

For example, what kinds of attractors may exist? Around which initial conditions is the system most sensitive? Are there any [fixed points](https://en.wikipedia.org/wiki/Fixed-point_theorem)?

## Acknowledgements
Shoutout to [Prof. Abigail Jacobs](https://azjacobs.com/) and her [Complex Systems](https://lsa.umich.edu/cscs) 501 class!