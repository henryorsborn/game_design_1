from core.battle.enemy import Enemy
from core.entities.player import Player

class BattleStats(object):

    def __init__(self, player: Player, in_battle: bool = True, battle_selection: int = 0, enemy_path: str = ""):
        self.player = player
        self.in_battle = in_battle
        self.battle_selection = battle_selection
        self.enemy_path = enemy_path
        self.enemy = None
        self.battle_queue = []

    def set_enemy_path(self, enemy_path):
        self.enemy_path = enemy_path
        self.enemy = Enemy.read_and_deserialize_yml(enemy_path)

    def set_battle_queue(self):
        queue = []

        strongest_enemy = max([self.player, self.enemy], key=lambda x: x.speed)
        weakest_enemy = min([self.player, self.enemy], key=lambda x: x.speed)
        adjusted_cooldown = strongest_enemy.speed/weakest_enemy.speed

        turns = [{"name":"Player","wait_time":int(self.player.speed/adjusted_cooldown),"cool_down":0},
                 {"name":self.enemy.name,"wait_time":int(self.enemy.speed/adjusted_cooldown),"cool_down":0}]

        for _ in range(100):
            for i in range(len(turns)):
                turns[i]["cool_down"] += 1
                if turns[i]["cool_down"] == turns[i]["wait_time"]:
                    turns[i]["cool_down"] = 0
                    queue.append(turns[i]["name"])
        self.battle_queue = queue
