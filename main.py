from environment import Environment
from item import Item
from action import Action

e = Environment(3, 3)
i = Item(20)
print(e)
e.place(i, 1, 1)
print(i.environment)
i.action = Action.RIGHT
e.update()
print(e)