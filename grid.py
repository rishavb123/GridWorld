from actions import *
from time import sleep
import numpy as np
from constants import *

class Grid:

    def __init__(self, rows, cols, start):
        self.rows = rows
        self.cols = cols
        self.start = start
        self.set_state(start) 

    def restart(self):
        self.set_state(self.start)

    def set(self, rewards, actions):
        self.rewards = rewards
        self.actions = actions

    def set_board(self, board):
        self.board = board
    
    def draw_board(self, symbol='A'):
        board_copy = [x.copy() for x in self.board]
        board_copy[self.i][self.j] = symbol
        for i in range(self.rows):
            print("------" * self.cols)
            for j in range(self.cols):
                a = board_copy[i][j]
                print("  %s  |" % a, end="")
            print("")
        print("------" * self.cols + "\n")

    def set_state(self, state):
        self.i = state[0]
        self.j = state[1]

    def set_start(self, state):
        self.start = state

    def random_start_position(self):
        self.set_start(list(self.all_states())[np.random.choice(len(self.all_states()))])

    def get_state(self):
        return (self.i,  self.j)

    def move(self, action):
        if action in self.actions[self.get_state()]:
            if action == UP:
                self.i -= 1
            elif action == DOWN:
                self.i += 1
            elif action == LEFT:
                self.j -= 1
            elif action == RIGHT:
                self.j += 1
        else:
            print('Not a valid action')
        return self.rewards.get(self.get_state(), 0)

    def undo_move(self, action):
        move(-action)

    def game_over(self):
        return self.get_state() not in self.actions

    def all_states(self):
        return set(self.actions.keys()) | set(self.rewards.keys())

    def is_terminal(self, state):
        return state not in self.actions

    def play(self, policy, delay=0.5, symbol='A', log=True):
        self.restart()
        if log:
            self.draw_board()
        total_reward = 0
        steps = 0
        states_and_rewards = []
        while not self.game_over():
            sleep(delay)
            r = self.move(policy[self.get_state()])
            s = self.get_state()
            states_and_rewards.append((s, r))
            steps += 1
            if log:
                print('Step: ', steps, '\tReward: ', r)
                self.draw_board(symbol=symbol)
            total_reward += r
        if log:
            print('\nTotal Number of Steps: ', steps)
            print('Total Reward: ', total_reward, '\n')

        states_and_returns = []
        G = 0
        first = True

        for s, r in reversed(states_and_rewards):
            if first:
                first = False
            else:
                states_and_returns.append((s, G))
            G = r + GAMMA * G

        states_and_returns.reverse()
        return states_and_returns

    @staticmethod
    def standard_grid():
        g = Grid(3, 4, (2, 0))
        rewards = { 
            (0, 3): 1,
            (1, 3): -1
        }
        actions = {
            (0, 0): (DOWN, RIGHT),
            (0, 1): (LEFT, RIGHT),
            (0, 2): (LEFT, DOWN, RIGHT),
            (1, 0): (UP, DOWN),
            (1, 2): (UP, DOWN, RIGHT),
            (2, 0): (UP, RIGHT),
            (2, 1): (LEFT, RIGHT),
            (2, 2): (LEFT, RIGHT, UP),
            (2, 3): (LEFT, UP)
        }
        g.set(rewards, actions)
        return g

    @staticmethod
    def negative_grid(step_cost=-0.1):
        g = Grid.standard_grid()
        g.rewards.update({
            (0, 0): step_cost,
            (0, 1): step_cost,
            (0, 2): step_cost,
            (1, 0): step_cost,
            (1, 2): step_cost,
            (2, 0): step_cost,
            (2, 1): step_cost,
            (2, 2): step_cost,
            (2, 3): step_cost
        })
        return g

    @staticmethod
    def load(filename, step_cost=-0.1, win_reward=1, lose_punishment=-1, bump_factor=10, money_reward=None):
        if money_reward == None:
            money_reward = -step_cost/2
        with open(filename) as file:
            s = file.read()
            lines = s.split('\n')
            actions = {}
            rewards = {}
            start = (0, 0)
            rows, cols = len(lines), len(lines[0])
            for i in range(rows):
                for j in range(cols):
                    s = (i, j)
                    c = lines[i][j]
                    current_reward = None
                    if c == 'S':
                        c = '_'
                        start = (i, j)
                    elif c == '~':
                        c = '_'
                        current_reward = bump_factor * step_cost
                    elif c == '$':
                        c = '_'
                        current_reward = money_reward
                    if c == '_':
                        a = []
                        if current_reward == None:
                            rewards[s] = step_cost
                        else:
                            rewards[s] = current_reward
                        motion_states = [
                            (i - 1, j),
                            (i + 1, j),
                            (i, j - 1),
                            (i, j + 1)
                        ]
                        for state_index in range(len(motion_states)):
                            state = motion_states[state_index]
                            if state[0] >= 0 and state[1] >= 0 and state[0] < rows and state[1] < cols and lines[state[0]][state[1]] in ['S', '$', '~', '_', '+', '-']:
                                a.append(ACTIONS[state_index])
                        actions[s] = a
                    elif c == '+':
                        rewards[s] = win_reward
                    elif c == '-':
                        rewards[s] = lose_punishment
            g = Grid(rows, cols, start)
            g.set(rewards, actions)
            board_symbols = {
                'S': ' ',
                '#': '#',
                '$': '$',
                '_': ' ',
                '-': '^',
                '~': 'n',
                '+': 'G'
            }
            g.set_board([[board_symbols[c] for c in l] for l in lines])
            return g