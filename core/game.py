from core.grid.grid import Grid
from core.game_state import GameState
from core.battle.battle_stats import BattleStats
from core.entities.player import Player


class Game(object):

    def __init__(self, grid: Grid):
        """
        :param grid: Grid
        """
        self.player = Player(grid.start_index)
        self.game_state = GameState(grid, BattleStats(player=self.player, in_battle=False))
