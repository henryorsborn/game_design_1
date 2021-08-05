from core.entities.entity import Entity


class Player(Entity):
    """The player character that the user will control"""

    def __init__(self, start_index: list):
        """
        :param start_index: list[int, int]
        """
        super().__init__(start_index)
        self.health = None  # todo
