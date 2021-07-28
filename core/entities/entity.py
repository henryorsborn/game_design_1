class Entity(object):
    """Any non static object that can be interacted with or has an animation. Placed on tiles"""

    def __init__(self, start_index: list):
        """
        :param start_index: list[int, int]
        """
        self.start_index = start_index