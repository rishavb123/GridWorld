import numpy as np

from grid import *
from actions import *
from constants import *
from util import *
from rl import iterative_policy_evaluation

grid = Grid.standard_grid()
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


V = iterative_policy_evaluation(grid, policy)
print("values:")
print_values(V, grid)
