from core.entities.player import Player
from core.entities.chest import Chest
from core.grid.blank_block import BlankBlock
from yaml import load


class Grid(object):
    """The set of tiles of each 'Room' in the game. It will contain the player, chests, npcs, and all other entities"""

    def __init__(self, width: int, height: int, blank_regions: list, entities: list, start_index: tuple):
        """
        :type width: int
        :type height: int
        :type blank_regions: list
        :type entities: list
        :type start_index: tuple
        """
        self.width = width
        self.height = height
        self.blank_regions = blank_regions
        self.entities = entities
        self.start_index = start_index


    # intended for testing purposes
    def __repr__(self):
        base_grid = [["_" for i in range(self.height)] for j in range(self.width)]
        for entity in self.entities:
            if type(entity)==Player:
                base_grid[entity.start_index[0]][entity.start_index[1]] = "P"
            if type(entity)==Chest:
                base_grid[entity.start_index[0]][entity.start_index[1]] = "C"
        for blank_region in self.blank_regions:
            for i in range(blank_region.height):
                for j in range(blank_region.width):
                    base_grid[i+blank_region.top_left_index[0]][j+blank_region.top_left_index[1]] = " "
        return "\n".join(["\t".join(row) for row in base_grid])

    @staticmethod
    def read_and_deserialize_yml(path: str):
        """
        :param path: str
        """
        with open(path) as file:
            content = load(file.read())["grid"]
        blank_regions = [BlankBlock((bb["blank_region"]["top_left_index_x"],bb["blank_region"]["top_left_index_y"]),bb["blank_region"]["width"],bb["blank_region"]["height"]) for bb in content["blank_regions"]]
        entities_unadjusted = content["entities"]
        entities = []
        for entity in entities_unadjusted:
            if entity["entity"]["type"] == "Player":
                entities.append(Player((entity["entity"]["start_index_x"],entity["entity"]["start_index_y"])))
            if entity["entity"]["type"] == "Chest":
                entities.append(Chest((entity["entity"]["start_index_x"],entity["entity"]["start_index_y"]),entity["entity"]["is_opened"]))
            else:
                pass
        return Grid(content["width"],content["height"],blank_regions,entities,(content["start_index_x"],content["start_index_y"]))