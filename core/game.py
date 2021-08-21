from core.grid.grid import Grid
from core.game_state import GameState
from core.battle.battle_stats import BattleStats


class Game(object):

    def __init__(self, grid: Grid):
        """
        :param grid: Grid
        """
        self.game_state = GameState(grid, BattleStats(in_battle=False))

