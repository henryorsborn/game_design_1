from core.entities.player import Player
from core.entities.chest import Chest
from core.grid.blank_block import BlankBlock
from core.constants.constants import SCALE, ENTITY_SCALE, BASE_ADJUST, ENTITY_ADJUST, PLAYER, EMPTY, CHEST, BLANK
from core.util.util import range_scale
from core.grid.tile import Tile
from yaml import load
import pygame


class Grid(object):
    """The set of tiles of each 'Room' in the game. It will contain the player, chests, npcs, and all other entities"""

    def __init__(self, width: int, height: int, blank_regions: list, entities: list, start_index: list,
                 player_position: list, enemy_paths: list, enemy_encounter_rates: list):
        """
        :type width: int
        :type height: int
        :type blank_regions: list
        :type entities: list
        :type start_index: list
        :type player_position: list
        """
        self.width = width
        self.height = height
        self.blank_regions = blank_regions
        self.entities = entities
        self.start_index = start_index
        self.player_position = player_position
        self.danger = 90
        self.tiles = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.enemy_paths = enemy_paths
        self.enemy_encounter_rates = enemy_encounter_rates
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

    # intended for testing purposes
    def __repr__(self):
        base_grid = [["_" for _ in range(self.height)] for _ in range(self.width)]
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
                    [content["start_index_x"], content["start_index_y"]], player_position,
                    list(map(lambda x: f"../resources/beastiary/{x['enemy']['path']}.yml", content["enemies"])),
                    list(map(lambda x: x['enemy']["encounter_rate"], content["enemies"])))

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

