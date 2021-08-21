class Attack(object):

    def __init__(self, name: str, key: str, damage: int, accuracy: int, cost: int, effect: list):
        self.name = name
        self.key = key
        self.damage = damage
        self.accuracy = accuracy
        self.cost = cost
        self.effect = effect
