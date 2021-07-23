from core.grid.grid import Grid

if __name__ == "__main__":
    grid = Grid.read_and_deserialize_yml("../resources/grid/example_room.yml")
    # grid should have player and chest on bottom row and the grid should have a missing 3x4 chunk missing from top left
    print(grid)