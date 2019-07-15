import numpy as np

from grid import *
from actions import *
from constants import *
from util import *
from rl import *

grid = Grid.load('./grids/standard_grid.txt')
S = grid.all_states()

print("rewards:")
print_values(grid.rewards, grid)

policy = {
    (2, 0): UP,
    (1, 0): UP,
    (0, 0): RIGHT,
    (0, 1): RIGHT,
    (0, 2): RIGHT,
    (1, 2): RIGHT,
    (2, 1): RIGHT,
    (2, 2): RIGHT,
    (2, 3): UP,
}

print("policy:")
print_policy(policy, grid)


V = monte_carlo(grid, policy, iterations=1000)
print("values:")
print_values(V, grid)
