from core.entities.entity import Entity


class Player(Entity):
    """The player character that the user will control"""

    def __init__(self, start_index: list):
        """
        :param start_index: list[int, int]
        """
        super().__init__(start_index)
        self.level = 1
        self.hp = 300
        self.max_hp = 300
        self.mp = 100
        self.strength = 5
        self.defense = 5
        self.magic = 5
        self.magic_defense = 5
        self.speed = 5
        self.luck = 5
        self.spl = []