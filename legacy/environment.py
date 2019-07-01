import numpy as np
from action import Action

class Environment:

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def place(self, item, x, y):
        self.items.append({ "item" : item })
        self.board[x][y] = item.placeholder
        item.intoEnvironment(self)

    def remove(self, x, y):
        self.items.remove(self.board[x][y])
        self.board[x][y] = 0

    def reward(self, item):
        return self.rewards[item.x][item.y]

    def update(self):
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                i = self.board[x][y]

    def __str__(self):
        s = ""
        for i in range(self.rows):
            for j in range(self.cols):
                s += str(self.board[i][j]) + "\t"
            s += "\n"
        return s