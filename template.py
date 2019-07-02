import numpy as np

from grid import *
from actions import *
from constants import *
from util import *
from rl import *

grid = Grid.load('./grids/maze2.txt', win_reward=10)

print("")

print("board:")
grid.draw_board()

print("rewards:")
print_values(grid.rewards, grid)

policy = init_random_policy(grid)

print("initial_policy:")
print_policy(policy, grid)

V = init_random_value_function(grid)
policy = init_random_policy(grid)

# Implement algorithm here

print("value_function:")
print_values(V, grid)

print("final_policy:")
print_policy(policy, grid)

if input('Would you like to see the agent play the maze? (Y / n): ').lower()[0] == 'y':
    grid.play(policy)