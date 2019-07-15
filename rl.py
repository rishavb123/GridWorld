import numpy as np

from grid import Grid
from constants import *
from actions import *

def init_random_policy(grid, policy={}):
    for s in grid.actions.keys():
        policy[s] = np.random.choice(grid.actions[s])
    return policy

def init_random_value_function(grid, V={}):
    for s in grid.all_states():
        if not grid.is_terminal(s):
            V[s] = np.random.random()
        else:
            V[s] = 0
    return V

def iterative_policy_evaluation(grid, policy, V={}):
    S = grid.all_states()
    while True:
        delta = 0
        for s in S:
            old_v = V.get(s, 0)
            if not grid.is_terminal(s):
                grid.set_state(s)
                a = policy[s]
                r = grid.move(a)
                next_v = V.get(grid.get_state(), 0)
                V[s] = r + GAMMA * next_v
                delta = max(delta, abs(V[s] - old_v))
            else:
                V[s] = 0
        if delta < EPSILON:
            break
    return V

def policy_iteration(grid, V, policy=None):
    if policy == None:
        policy = init_random_policy(grid)
    is_policy_converged = True
    for s in grid.all_states():
        if s in policy:
            old_a = policy[s]
            new_a = None
            best_value = float('-inf')
            for a in grid.actions[s]:
                grid.set_state(s)
                r = grid.move(a)
                v = r + GAMMA * V.get(grid.get_state(), 0)
                if v > best_value:
                    best_value = v
                    new_a = a
            policy[s] = new_a
            if new_a != old_a:
                is_policy_converged = False
    return policy, is_policy_converged

def value_iteration(grid, V={}):
    while True:
        delta = 0
        for s in grid.all_states():
            if grid.is_terminal(s):
                V[s] = 0
            else:
                old_v = V.get(s, 0)
                new_v = float('-inf')
                for a in grid.actions[s]:
                    grid.set_state(s)
                    r = grid.move(a)
                    v = r + GAMMA * V.get(grid.get_state(), 0)
                    if v > new_v:
                        new_v = v
                V[s] = new_v
                delta = max(delta, abs(new_v - old_v))
        if delta < EPSILON:
            break
    return V

def monte_carlo(grid, policy, V={}, iterations=1000):
    returns = {}
    for _ in range(iterations):
        grid.random_start_position()
        states_and_returns = grid.play(policy, delay=0, log=False)
        seen_states = set()
        for s, G in states_and_returns:
            if s not in seen_states:
                if s in returns.keys():
                    returns[s].append(G)
                else:
                    returns[s] = [G]
                V[s] = np.mean(returns[s])
                seen_states.add(s)
    return V