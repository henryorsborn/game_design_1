from core.entities.entity import Entity


class Chest(Entity):

    def __init__(self, start_index: tuple, is_opened: bool = False):
        """
        :param start_index: tuple(int, int)
        :param is_opened: bool
        """
        super().__init__(start_index)
        self.is_opened = is_opened
        self.item = None
