from core.grid.grid import Grid
from core.entities.player import Player
from core.entities.chest import Chest
from core.grid.blank_block import BlankBlock
from pygame.locals import *
import pygame
import time

if __name__ == "__main__":
    grid = Grid.read_and_deserialize_yml("../resources/grid/example_room.yml")
    # grid should have player and chest on bottom row and the grid should have a missing 3x4 chunk missing from top left
    print(grid)
    screen = pygame.display.set_mode((500, 400))
    grid.repaint(screen)
    moving = False
    current_event = None
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == KEYDOWN:
                if event.key in [pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d]:
                    current_event = event
                    moving = True
            if event.type == KEYUP:
                moving = False
        if moving:
            pygame.display.update()
            grid.move_player(current_event, screen)
            time.sleep(0.15)
        pygame.display.update()