from typing import Optional

from core.beam import Beam
from core.direction import Direction
from core.point import Point
from core.std_vals import *


class Edge:
    """
    A class to represent an edge of a osm way.

    Args
    ----
    point1 : Point
        coordinates of the first end
    point2 : Point
        coordinates of the second end

    Attributes
    ----------
    p1 : Point
        coordinates of the first end
    p2 : Point
        coordinates of the second end
    """

    def __init__(self, point1: Point, point2: Point):
        if point1 == point2:
            raise RuntimeError("Edge cannot consist of two different points!\n" + str(self))
        self.p1: Point = point1
        self.p2: Point = point2

    def __eq__(self, other):
        return self.p1 == other.p1 and self.p2 == other.p2

    def __len__(self) -> float:
        return len(self.dir)

    def __repr__(self):
        return "{} -- {}".format(self.p1, self.p2)

    @property
    def points(self) -> tuple[Point, Point]:
        """
        Returns both end points that define the edge.
        """
        return self.p1, self.p2

    @property
    def dir(self) -> Direction:
        """
        Returns a direction object running from point 1 to point 2.
        """
        return Direction.from_points(self.p1, self.p2)

    @property
    def middle_point(self) -> Point:
        """
        Returns the middle point of the edge.
        """
        return Point((self.p1.x + self.p2.x) / 2, (self.p1.y + self.p2.y) / 2)

    def to_beam(self) -> Beam:
        """
        Converts the edge into a beam instance starting at p1.
        """
        return Beam(self.p1, self.dir)

    def contains_point(self, pt: Point, tolerance=std_tolerance) -> bool:
        """
        Checks whether a point is on or very near the edge.
        """
        # check whether point equals end points
        if pt == self.p1:
            return True
        if pt == self.p2:
            return True

        # check whether point is in possible edge's x and y boundary
        if not (min(self.p1.x, self.p2.x) <= pt.x <= max(self.p1.x, self.p2.x)) \
                or not (min(self.p1.y, self.p2.y) <= pt.y <= max(self.p1.y, self.p2.y)):
            return False

        # find the closest point from the given point to the edges beam
        closest_point_on_edge = self.intersection_with_beam(Beam(pt, self.dir.perpendicular()))
        # ... and check for equality
        if Point.are_close(closest_point_on_edge, pt, tolerance):
            return True

        return False

    def intersection_with_beam(self, beam: Beam) -> Optional[Point]:
        """
        Calculates the intersection point of a beam hitting the edges beam if only one exists.
        """
        return Beam.intersection(self.to_beam(), beam)
