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
        self.mp = 100
        self.str = 5
        self.def_ = 5
        self.mag = 5
        self.mgdf = 5
        self.spd = 5
        self.luck = 5
        self.spl = []