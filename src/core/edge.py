from core.beam import Beam
from core.direction import Direction
from core.point import Point


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
