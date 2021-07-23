from core.grid.grid import Grid
from core.entities.player import Player
from core.entities.chest import Chest
from core.grid.blank_block import BlankBlock
import pygame
from pygame.locals import *

SCALE = 25
ENTITY_SCALE = 15
BASE_ADJUST = 40
ENTITY_ADJUST = 45


def range_scale(stop):
    return range(0,stop*SCALE,SCALE)

if __name__ == "__main__":
    grid = Grid.read_and_deserialize_yml("../resources/grid/example_room.yml")
    # grid should have player and chest on bottom row and the grid should have a missing 3x4 chunk missing from top left
    print(grid)
    screen = pygame.display.set_mode((500, 400))
    for i in range_scale(grid.height):
        for j in range_scale(grid.width):
            pygame.draw.rect(screen, (100, 100, 255), (i+BASE_ADJUST, j+BASE_ADJUST, SCALE, SCALE))
    for entity in grid.entities:
        if type(entity) == Player:
            pygame.draw.rect(screen, (200, 100, 0), ((entity.start_index[1]*SCALE)+ENTITY_ADJUST, (entity.start_index[0]*SCALE)+ENTITY_ADJUST, ENTITY_SCALE, ENTITY_SCALE))
        if type(entity) == Chest:
            pygame.draw.rect(screen, (0, 255, 100), ((entity.start_index[1]*SCALE)+ENTITY_ADJUST, (entity.start_index[0]*SCALE)+ENTITY_ADJUST, ENTITY_SCALE, ENTITY_SCALE))
    for blank_region in grid.blank_regions:
        for i in range_scale(blank_region.height):
            for j in range_scale(blank_region.width):
                delta_x = i + (blank_region.top_left_index[0]*SCALE) + BASE_ADJUST
                delta_y = j + (blank_region.top_left_index[1]*SCALE) + BASE_ADJUST
                pygame.draw.rect(screen, (0, 0, 0), (delta_x, delta_y, SCALE, SCALE))
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            pygame.display.update()