from core.vec2 import Vec2


class Point(Vec2):
    """
    A class to represent a geographical point with two coordinates.

    Args
    ----
    x : float
        the first coordinate (longitude)
    y : float
        the second coordinate (latitude)

    Attributes
    ----------
    x : float
        the first coordinate (longitude)
    y : float
        the second coordinate (latitude)
    """

    def __init__(self, x: float, y: float):
        super().__init__(x, y)
