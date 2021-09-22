class Attack(object):

    def __init__(self, name: str, key: str, dmg: int, acc: int, cost: int, eff: list = None):
        self.name = name
        self.key = key
        self.damage = dmg
        self.accuracy = acc
        self.cost = cost
        if not eff:
            eff = []
        self.effect = eff
