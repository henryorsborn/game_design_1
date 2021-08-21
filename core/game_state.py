from core.grid.grid import Grid
from core.battle.battle_stats import BattleStats
import pygame
import time
import random
from core.constants.constants import EMPTY


class GameState(object):

    def __init__(self, grid: Grid, battle_stats: BattleStats):
        self.grid = grid
        self.battle_stats = battle_stats
        self.font = None

    def set_font(self, font: pygame.font):
        self.font = font

    @staticmethod
    def paint_battle_start_animation(screen: pygame.Surface):
        for i in range(0, 500, 10):
            for j in range(10, 500, 30):
                if j % 20 == 0:
                    pygame.draw.rect(screen, (255, 100, 100), (j, 470 - i, 10, 10))
                    pygame.draw.rect(screen, (255, 100, 100), (500 - i, j, 10, 10))
                else:
                    pygame.draw.rect(screen, (255, 100, 100), (j, i, 10, 10))
                    pygame.draw.rect(screen, (255, 100, 100), (i, j, 10, 10))
            time.sleep(0.03)
            pygame.display.update()
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 500, 500))

    def paint_battle_menu(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (255, 255, 255), (60, 225, 240, 100))
        pygame.draw.rect(screen, (0, 0, 0), (65, 230, 230, 90))
        commands = ['Attack', 'Skill', 'Magic', 'Item']
        indexes = [(90, 235), (90, 257), (90, 278), (90, 300)]
        for i in range(len(commands)):
            if i == self.battle_stats.battle_selection:
                adjusted_index = (indexes[i][0] - 20, indexes[i][1])
                screen.blit(self.font.render(f"* {commands[i]}", False, (255, 128, 128)), adjusted_index)
            else:
                screen.blit(self.font.render(commands[i], False, (255, 255, 255)), indexes[i])

    # fixme work on indexes
    def move_player(self, key_event: pygame.event, screen: pygame.Surface):
        if key_event.key == pygame.K_w:
            if self.grid.player_position[0] != 0:
                if self.grid.tiles[self.grid.player_position[1]][self.grid.player_position[0] - 1].type_ == EMPTY:
                    self.grid.tiles[self.grid.player_position[1]][self.grid.player_position[0]].type_ = EMPTY
                    self.grid.player_position[0] -= 1
        elif key_event.key == pygame.K_a:
            if self.grid.player_position[1] != 0:
                if self.grid.tiles[self.grid.player_position[1] - 1][self.grid.player_position[0]].type_ == EMPTY:
                    self.grid.tiles[self.grid.player_position[1]][self.grid.player_position[0]].type_ = EMPTY
                    self.grid.player_position[1] -= 1
        elif key_event.key == pygame.K_s:
            if self.grid.player_position[0] != self.grid.width - 1:
                if self.grid.tiles[self.grid.player_position[1]][self.grid.player_position[0] + 1].type_ == EMPTY:
                    self.grid.tiles[self.grid.player_position[1]][self.grid.player_position[0]].type_ = EMPTY
                    self.grid.player_position[0] += 1
        elif key_event.key == pygame.K_d:
            if self.grid.player_position[1] != self.grid.height - 1:
                if self.grid.tiles[self.grid.player_position[1] + 1][self.grid.player_position[0]].type_ == EMPTY:
                    self.grid.tiles[self.grid.player_position[1]][self.grid.player_position[0]].type_ = EMPTY
                    self.grid.player_position[1] += 1
        self.grid.repaint(screen)
        if random.randint(0, 100 - self.grid.danger) % (100 - self.grid.danger) == 0 and self.grid.danger != 0:
            self.initiate__battle(screen)

    def initiate__battle(self, screen: pygame.Surface):
        GameState.paint_battle_start_animation(screen)
        self.paint_battle_menu(screen)
        self.battle_stats.enemy_path = random.choices(self.grid.enemy_paths, self.grid.enemy_encounter_rates, k=1)[0]
        self.battle_stats.in_battle = True
