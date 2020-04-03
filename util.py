from actions import *

def print_values(V, g):
    for i in range(g.rows):
        print("------" * g.cols)
        for j in range(g.cols):
            v = V.get((i,j), 0)
            if v >= 0:
                print(" %.2f|" % v, end="")
            else:
                print("%.2f|" % v, end="") # - sign takes up an extra space
        print("")
    print("------" * g.cols + "\n")

def print_policy(P, g):
    for i in range(g.rows):
        print("------" * g.cols)
        for j in range(g.cols):
            a = ' '
            try:
                a = ACTION_SYMBOLS[P.get((i,j), ' ')]
            except:
                pass
            print("  %s  |" % a, end="")
        print("")
    print("------" * g.cols + "\n")

def max_dict(d):
    max_key = None
    max_val = float('-inf')
    for k, v in d.items():
        if v > max_val:
            max_val = v
            max_key = k
    return max_key, max_val

