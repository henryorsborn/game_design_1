from core.entities.player import Player
from core.entities.chest import Chest
from core.grid.blank_block import BlankBlock
from core.constants.constants import SCALE, ENTITY_SCALE, BASE_ADJUST, ENTITY_ADJUST, PLAYER, EMPTY, CHEST, BLANK
from core.util.util import range_scale
from core.grid.tile import Tile
import time
from yaml import load
import random
import pygame


class Grid(object):
    """The set of tiles of each 'Room' in the game. It will contain the player, chests, npcs, and all other entities"""

    def __init__(self, width: int, height: int, blank_regions: list, entities: list, start_index: tuple,
                 player_position: list):
        """
        :type width: int
        :type height: int
        :type blank_regions: list
        :type entities: list
        :type start_index: tuple
        :type player_position: list
        """
        self.width = width
        self.height = height
        self.blank_regions = blank_regions
        self.entities = entities
        self.start_index = start_index
        self.player_position = player_position
        self.danger = 89
        self.in_battle = False
        self.tiles = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.font = None
        for i in range(self.height):
            for j in range(self.width):
                self.tiles[i][j] = Tile(EMPTY)
        for entity in self.entities:
            if type(entity) == Player:
                self.tiles[entity.start_index[1]][entity.start_index[0]] = Tile(PLAYER)
            if type(entity) == Chest:
                self.tiles[entity.start_index[1]][entity.start_index[0]] = Tile(CHEST)
        for blank_region in self.blank_regions:
            for i in range(blank_region.height):
                for j in range(blank_region.width):
                    self.tiles[i + blank_region.top_left_index[0]][j + blank_region.top_left_index[1]] = Tile(BLANK)
        # todo optimize other functions using player_position

    def set_font(self, font: pygame.font):
        self.font = font

    # intended for testing purposes
    def __repr__(self):
        base_grid = [["_" for i in range(self.height)] for j in range(self.width)]
        for entity in self.entities:
            if type(entity) == Player:
                base_grid[entity.start_index[0]][entity.start_index[1]] = "P"
            if type(entity) == Chest:
                base_grid[entity.start_index[0]][entity.start_index[1]] = "C"
        for blank_region in self.blank_regions:
            for i in range(blank_region.height):
                for j in range(blank_region.width):
                    base_grid[i + blank_region.top_left_index[0]][j + blank_region.top_left_index[1]] = " "
        return "\n".join(["\t".join(row) for row in base_grid])

    @staticmethod
    def read_and_deserialize_yml(path: str):
        """
        :param path: str
        """
        with open(path) as file:
            content = load(file.read())["grid"]
        blank_regions = [BlankBlock((bb["blank_region"]["top_left_index_x"], bb["blank_region"]["top_left_index_y"]),
                                    bb["blank_region"]["width"], bb["blank_region"]["height"]) for bb in
                         content["blank_regions"]]
        entities_unadjusted = content["entities"]
        entities = []
        player_position = [0, 0]
        for entity in entities_unadjusted:
            if entity["entity"]["type"] == "Player":
                player_position = [entity["entity"]["start_index_x"], entity["entity"]["start_index_y"]]
                entities.append(Player(player_position))
            if entity["entity"]["type"] == "Chest":
                entities.append(Chest((entity["entity"]["start_index_x"], entity["entity"]["start_index_y"]),
                                      entity["entity"]["is_opened"]))
            else:
                pass
        return Grid(content["width"], content["height"], blank_regions, entities,
                    (content["start_index_x"], content["start_index_y"]), player_position)

    def repaint(self, screen: pygame.Surface):
        for i in range_scale(self.height):
            for j in range_scale(self.width):
                pygame.draw.rect(screen, (100, 100, 255), (i + BASE_ADJUST, j + BASE_ADJUST, SCALE, SCALE))
        for entity in self.entities:
            if type(entity) == Chest:
                pygame.draw.rect(screen, (0, 255, 100), (
                (entity.start_index[1] * SCALE) + ENTITY_ADJUST, (entity.start_index[0] * SCALE) + ENTITY_ADJUST,
                ENTITY_SCALE, ENTITY_SCALE))
        for blank_region in self.blank_regions:
            for i in range_scale(blank_region.height):
                for j in range_scale(blank_region.width):
                    delta_x = i + (blank_region.top_left_index[0] * SCALE) + BASE_ADJUST
                    delta_y = j + (blank_region.top_left_index[1] * SCALE) + BASE_ADJUST
                    pygame.draw.rect(screen, (0, 0, 0), (delta_x, delta_y, SCALE, SCALE))
        pygame.draw.rect(screen, (200, 100, 0), (
            (self.player_position[1] * SCALE) + ENTITY_ADJUST, (self.player_position[0] * SCALE) + ENTITY_ADJUST,
            ENTITY_SCALE, ENTITY_SCALE))

    def paint_battle_start_animation(self, screen: pygame.Surface):
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
        # todo add these dynamically
        screen.blit(self.font.render('Attack', False, (255, 255, 255)), (70, 235))
        screen.blit(self.font.render('Skill', False, (255, 255, 255)), (70, 257))
        screen.blit(self.font.render('Magic', False, (255, 255, 255)), (70, 278))
        screen.blit(self.font.render('Item', False, (255, 255, 255)), (70, 300))

    # fixme work on indexes
    def move_player(self, key_event: pygame.event, screen: pygame.Surface):
        if key_event.key == pygame.K_w:
            if self.player_position[0] != 0:
                if self.tiles[self.player_position[1]][self.player_position[0] - 1].type_ == EMPTY:
                    self.tiles[self.player_position[1]][self.player_position[0]].type_ = EMPTY
                    self.player_position[0] -= 1
        elif key_event.key == pygame.K_a:
            if self.player_position[1] != 0:
                if self.tiles[self.player_position[1] - 1][self.player_position[0]].type_ == EMPTY:
                    self.tiles[self.player_position[1]][self.player_position[0]].type_ = EMPTY
                    self.player_position[1] -= 1
        elif key_event.key == pygame.K_s:
            if self.player_position[0] != self.width - 1:
                if self.tiles[self.player_position[1]][self.player_position[0] + 1].type_ == EMPTY:
                    self.tiles[self.player_position[1]][self.player_position[0]].type_ = EMPTY
                    self.player_position[0] += 1
        elif key_event.key == pygame.K_d:
            if self.player_position[1] != self.height - 1:
                if self.tiles[self.player_position[1] + 1][self.player_position[0]].type_ == EMPTY:
                    self.tiles[self.player_position[1]][self.player_position[0]].type_ = EMPTY
                    self.player_position[1] += 1
        self.repaint(screen)
        if random.randint(0, 100 - self.danger) % (100 - self.danger) == 0:
            self.initiate__battle(screen)

    def initiate__battle(self, screen: pygame.Surface):
        self.paint_battle_start_animation(screen)
        self.paint_battle_menu(screen)
        self.in_battle = True
