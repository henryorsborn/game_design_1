class Entity(object):
    """Any non static object that can be interacted with or has an animation. Placed on tiles"""

    def __init__(self, start_index: tuple):
        """
        :param start_index: tuple(int, int)
        """
        self.start_index = start_index