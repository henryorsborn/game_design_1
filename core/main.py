from core import *
from pygame.locals import *
import pygame
import time

if __name__ == "__main__":
    grid = Grid.read_and_deserialize_yml("../resources/grid/example_room.yml")
    # grid should have player and chest on bottom row and the grid should have a missing 3x4 chunk missing from top left
    game = Game(grid)
    gs = game.game_state
    screen = pygame.display.set_mode((500, 400))
    gs.grid.repaint(screen)
    moving_x = False
    moving_y = False
    pygame.font.init()
    font = pygame.font.SysFont('Courier New', 13)
    gs.set_font(font)
    current_event = None
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if not gs.battle_stats.in_battle:
                if event.type == KEYDOWN:
                    if event.key in [pygame.K_a, pygame.K_d]:
                        current_event = event
                        moving_x = True
                    if event.key in [pygame.K_w, pygame.K_s]:
                        current_event = event
                        moving_y = True
                if event.type == KEYUP:
                    if event.key in [pygame.K_a, pygame.K_d]:
                        moving_x = False
                    if event.key in [pygame.K_w, pygame.K_s]:
                        moving_y = False
                if moving_x or moving_y:
                    gs.move_player(current_event, screen)
                    pygame.display.flip()
                    time.sleep(0.15)
            elif gs.battle_stats.current_turn == "Player":
                if event.type == KEYDOWN:
                    if event.key == pygame.K_s:
                        gs.battle_stats.battle_selection += 1
                        if gs.battle_stats.battle_selection == 4:
                            gs.battle_stats.battle_selection = 0
                    if event.key == pygame.K_w:
                        gs.battle_stats.battle_selection -= 1
                        if gs.battle_stats.battle_selection == -1:
                            gs.battle_stats.battle_selection = 3
                    if event.key == pygame.K_RETURN:
                        if gs.battle_stats.battle_selection == 0:
                            gs.attack(screen)
                    gs.paint_battle_menu(screen)
        pygame.display.flip()
