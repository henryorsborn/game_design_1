from core.battle.enemy import Enemy

class BattleStats(object):

    def __init__(self, in_battle: bool = True, battle_selection: int = 0, enemy_path: str = ""):
        self.in_battle = in_battle
        self.battle_selection = battle_selection
        self.enemy_path = enemy_path
        self.enemy = None

    def set_enemy_path(self, enemy_path):
        self.enemy_path = enemy_path
        self.enemy = Enemy.read_and_deserialize_yml(enemy_path)
