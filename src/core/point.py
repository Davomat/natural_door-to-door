import math

from core.std_vals import std_tolerance


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
               and math.isclose(self.x, other.x, abs_tol=std_tolerance) \
               and math.isclose(self.y, other.y, abs_tol=std_tolerance)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __repr__(self):
        return f'({round(self.x, 3)}|{round(self.y, 3)})'

    @staticmethod
    def are_close(p1, p2, tol) -> bool:
        """
        Checks if two points are within the given tolerance close to each other.
        """
        return math.isclose(p1.x, p2.x, abs_tol=tol) and math.isclose(p1.y, p2.y, abs_tol=tol)
