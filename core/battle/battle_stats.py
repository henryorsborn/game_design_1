class BattleStats(object):

    def __init__(self, in_battle: bool = True, battle_selection: int = 0, enemy_path: str = ""):
        self.in_battle = in_battle
        self.battle_selection = battle_selection
        self.enemy_path = enemy_path
