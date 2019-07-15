from grid import Grid

grid = Grid.standard_grid()

print(grid.start)
for _ in range(10):
    grid.random_start_position()
    print(grid.start)