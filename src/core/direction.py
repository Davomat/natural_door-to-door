import math

from core.point import Point
from core.std_vals import *
from core.vec2 import Vec2


class Direction(Vec2):
    """
    A class to represent a direction on the x-y-plane.

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
        if x == 0 and y == 0:
            raise RuntimeError("Cannot create a direction vector with length 0:\n" + str(self))

    def __eq__(self, other: 'Direction'):
        d1 = self.normalized()
        d2 = other.normalized()
        return (math.isclose(d1.x, d2.x, abs_tol=tolerance) and math.isclose(d1.y, d2.y, abs_tol=tolerance)) or \
               (math.isclose(d1.x, -d2.x, abs_tol=tolerance) and math.isclose(d1.y, -d2.y, abs_tol=tolerance))

    def __len__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __repr__(self):
        return f' -> {Point(self.x, self.y)}'

    @property
    def angle(self) -> float:
        """
        Calculates the mathematical angle of the direction vector (x y).
        """
        d = self.normalized()
        return math.copysign(math.acos(d.x) * 180 / math.pi, d.y) % 360

    def _inv_len(self) -> float:
        """
        Calculates the inverse of the length of the vector.
        """
        vec_len_sqr = self.x ** 2 + self.y ** 2
        return vec_len_sqr ** -0.5

    def _normalize(self):
        """
        Adjusts the length of the x and y values so that the length of the (x y) vector is 1.
        """
        inv_len = self._inv_len()
        self.x *= inv_len
        self.y *= inv_len

    def normalized(self) -> 'Direction':
        """
        Returns a new instance of the direction with a length of 1.
        """
        new_dir = Direction(self.x, self.y)
        new_dir._normalize()
        return new_dir

    def _naturalize(self, nat_dist: float):
        """
        Adjusts the length of the x and y values so that the length of the (x y) vector is the given nat_dist.
        """
        self._normalize()
        self.x *= nat_dist
        self.y *= nat_dist

    def naturalized(self, nat_dist: float) -> 'Direction':
        """
        Returns a new instance of the direction with a length of the given nat_dist.
        """
        new_dir = self.normalized()
        new_dir._naturalize(nat_dist)
        return new_dir

    def perpendicular(self) -> 'Direction':
        """
        Returns a new instance of a direction orthogonal (mathematical positive) to given one.
        """
        return Direction(-self.y, self.x)

    @staticmethod
    def from_points(p1: Point, p2: Point) -> 'Direction':
        """
        Returns a new instance of a Direction that runs from p1 to p2.
        """
        return Direction(p2.x - p1.x, p2.y - p1.y)
