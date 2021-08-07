from core.grid.grid import Grid
from core.battle.battle_stats import BattleStats


class GameState(object):

    def __init__(self, grid: Grid, battle_stats: BattleStats):
        self.grid = grid
        self.battle_stats = battle_stats
