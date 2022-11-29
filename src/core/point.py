import math

from core.std_vals import tolerance


class Point:
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
        self.x = x
        self.y = y

    def __eq__(self, other):
        return other is not None \
               and math.isclose(self.x, other.x, abs_tol=tolerance) \
               and math.isclose(self.y, other.y, abs_tol=tolerance)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __repr__(self):
        return f'({round(self.x, 3)}|{round(self.y, 3)})'
