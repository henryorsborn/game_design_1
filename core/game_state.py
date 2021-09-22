from core.grid.grid import Grid
from core.battle.battle_stats import BattleStats
import pygame
import time
import random
from core.constants.constants import EMPTY, WHITE, BLACK, RED, PINK, PINK2


class GameState(object):

    def __init__(self, grid: Grid, battle_stats: BattleStats):
        self.grid = grid
        self.battle_stats = battle_stats
        self.font = None

    def set_font(self, font: pygame.font):
        self.font = font

    @staticmethod
    def clear_screen(screen: pygame.Surface):
        pygame.draw.rect(screen, BLACK, (0, 0, 500, 500))

    @staticmethod
    def paint_battle_start_animation(screen: pygame.Surface):
        for i in range(0, 500, 10):
            for j in range(10, 500, 30):
                if j % 20 == 0:
                    pygame.draw.rect(screen, PINK, (j, 470 - i, 10, 10))
                    pygame.draw.rect(screen, PINK, (500 - i, j, 10, 10))
                else:
                    pygame.draw.rect(screen, PINK, (j, i, 10, 10))
                    pygame.draw.rect(screen, PINK, (i, j, 10, 10))
            time.sleep(0.03)
            pygame.display.update()
        GameState.clear_screen(screen)

    def paint_battle_menu(self, screen: pygame.Surface):
        pygame.draw.rect(screen, WHITE, (60, 225, 240, 100))
        pygame.draw.rect(screen, BLACK, (65, 230, 230, 90))
        pygame.draw.rect(screen, WHITE, (350, 225, 140, 100))
        pygame.draw.rect(screen, BLACK, (355, 230, 130, 90))
        commands = ['Attack', 'Skill', 'Magic', 'Item']
        command_indices = [235, 257, 278, 300]
        queue_indices = [302, 290, 278, 266, 254, 242, 230]
        for i in range(len(commands)):
            if i == self.battle_stats.battle_selection and self.battle_stats.current_turn == "Player":
                adjusted_index = (70, command_indices[i])
                screen.blit(self.font.render(f"* {commands[i]}", False, PINK2), adjusted_index)
            else:
                screen.blit(self.font.render(commands[i], False, WHITE), (70, command_indices[i]))
        if self.battle_stats.enemy:
            enemy_image = pygame.image.load(self.battle_stats.enemy.path_to_sprite)
            screen.blit(enemy_image, (300, 50))
        screen.blit(self.font.render(">>", False, RED), (360, 302))
        for i in range(6, -1, -1):
            screen.blit(self.font.render(self.battle_stats.battle_queue[i], False, WHITE), (380, queue_indices[i]))

    # fixme work on indices
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

    def attack(self, screen: pygame.Surface):
        luck = self.battle_stats.player.luck
        # with max luck the highest probability should be 99
        if 69 + int(luck*0.1176) > random.randint(1, 100):
            damage = round(self.battle_stats.player.strength * self.battle_stats.player.level * 3.9607 * (1+random.random()))
            self.battle_stats.enemy.hp -= damage
            self.battle_stats.end_turn()
            self.paint_battle_menu(screen)
            self.show_damage(damage, screen)
        else:
            pass

    def show_damage(self, damage: int, screen: pygame.Surface):
        self.paint_battle_menu(screen)
        for i in range(3):
            screen.blit(self.font.render(str(damage), False, WHITE), ((i*30)+230, 190))
            time.sleep(0.01)
            GameState.clear_screen(screen)
            self.paint_battle_menu(screen)
            time.sleep(0.01)
        GameState.clear_screen(screen)
        self.paint_battle_menu(screen)

    def initiate__battle(self, screen: pygame.Surface):
        self.battle_stats.in_battle = True
        GameState.paint_battle_start_animation(screen)
        self.battle_stats.set_enemy_path(random.choices(self.grid.enemy_paths, self.grid.enemy_encounter_rates, k=1)[0])
        self.battle_stats.set_battle_queue()
        self.paint_battle_menu(screen)
