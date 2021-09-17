class Attack(object):

    def __init__(self, name: str, key: str, damage: int, accuracy: int, cost: int = 0, effect: list = None):
        self.name = name
        self.key = key
        self.damage = damage
        self.accuracy = accuracy
        self.cost = cost
        if not effect:
            effect = []
        self.effect = effect
