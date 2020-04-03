import numpy as np
import matplotlib.pyplot as plt

from grid import *
from actions import *
from constants import *
from util import *
from rl import *

grid = Grid.standard_grid()

print("")

# print("board:")
# grid.draw_board()

print("rewards:")
print_values(grid.rewards, grid)

# initialize Q(s, a)
Q = {}
states = grid.all_states()

for s in states:
    Q[s] = {}
    for a in ACTIONS:
        Q[s][a] = 0

# let's also keep track of how many times Q[s] has been updated
update_counts = {}
update_counts_sa = {}

for s in states:
    update_counts_sa[s] = {}
    for a in ACTIONS:
        update_counts_sa[s][a] = 1.0

# repeat until convergence
t = 1.0
deltas = []
for iteration in range(1000):
    if iteration % 100 == 0:
        t += 1e-2
    if iteration % 2000 == 0:
        print("iteration:", iteration)

    s = (2, 0) # start state
    grid.set_state(s)

    a = max_dict(Q[s])[0] if np.random.random() < 1 - EPSILON else np.random.choice(ACTIONS)
    biggest_change = 0

    while not grid.game_over():
        r = grid.move(a)
        s2 = grid.get_state()

        a2 = max_dict(Q[s2])[0] if np.random.random() < 1 - EPSILON else np.random.choice(ACTIONS)

        alpha = ALPHA / update_counts_sa[s][a]
        update_counts_sa[s][a] += 0.005

        old_qsa = Q[s][a]
        Q[s][a] = Q[s][a] + alpha * (r + GAMMA * Q[s2][a2] - Q[s][a])
        biggest_change = max(biggest_change, np.abs(old_qsa - Q[s][a]))

        update_counts[s] = update_counts.get(s, 0) + 1

        s = s2
        a = a2
    
    deltas.append(biggest_change)

plt.plot(deltas)
plt.show()

policy = {}
V = {}
for s in grid.actions.keys():
    a, max_q = max_dict(Q[s])
    policy[s] = a
    V[s] = max_q

print("values:")
print_values(V, grid)
print("policy:")
print_policy(policy, grid)