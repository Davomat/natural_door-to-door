from core.corner import Corner
from core.edge import Edge
from core.point import Point


class Polygon:
    """
    A class to represent a two-dimensional polygon.

    Args
    ----
    points : list[Point]
        The points that create the outer shell of the polygon.
    is_room : bool
        The flag that determines the use of the polygon as a room (outer boundary) or a barrier (inner boundary).

    Attributes
    ----------
    points : list[Point]
        The points that stretch out the outer shell of the polygon.
    edges : list[Edge]
        The edges that are the outer shell of the polygon.
    corners : list[Corner]
        The corners of the outer shell.
    """

    def __init__(self, points: list[Point], is_room):
        self.points: list[Point] = points
        self._check_points()
        self.edges: list[Edge] = self._get_edges()
        self.corners: list[Corner] = self._get_corners()
        if (is_room and not self._is_counterclockwise) or (not is_room and self._is_counterclockwise):
            self._reverse()

    def __len__(self) -> int:
        return len(self.points)

    def __repr__(self) -> str:
        return repr(self.points)

    def _check_points(self):
        """
        Checks out point list to find corrupt or useless points in a polygon.
        """
        self._check_points_for_repetitions()
        self._check_points_for_straight_corners()

        # also test if polygon exists
        if len(self) < 3:
            raise RuntimeError('Polygon ' + str(self) + ' must consist of at least 3 not-aligned points.')

    def _check_points_for_repetitions(self):
        """
        Checks out point list and deletes every second of two consecutive points if they are equal.
        """
        for i in reversed(range(1, len(self) + 1)):
            if self.points[i % len(self)] == self.points[i - 1]:
                self.points.pop(i % len(self))

    def _check_points_for_straight_corners(self):
        """
        Checks out point list and deletes points that would lead to a straight (180°) corner.
        """
        for i in reversed(range(1, len(self) + 2)):
            if Edge(self.points[i % len(self)], self.points[i - 2]).cuts_point(self.points[(i - 1) % len(self)]):
                self.points.pop((i - 1) % len(self))

    def _get_edges(self) -> list[Edge]:
        """
        Calculates the edges of the polygon.
        """
        return [Edge(self.points[i], self.points[(i + 1) % len(self)]) for i in range(len(self))]

    def _get_corners(self) -> list[Corner]:
        """
        Calculates the corners of the polygon.
        """
        return [Corner(self.edges[i], self.edges[(i + 1) % len(self)]) for i in range(len(self))]

    @property
    def _is_counterclockwise(self) -> bool:
        """
        Checks whether the points of the polygon are given in a counterclockwise order.
        """
        result = 0.
        for corner in self.corners:
            result += corner.angle - 180.

        # result should sum up to -360 for counterclockwise and +360 for clockwise
        if -359. > result > -361.:
            return True
        if 359. < result < 361.:
            return False

        # raise error if polygon is still corrupted
        raise RuntimeError('Polygon ' + str(self) + ' is corrupted, probably not closed! angle: ' + str(result))

    def _reverse(self):
        """
        Reverses the sequence of the points the polygon consists of.
        """
        self.points.reverse()
        self.edges = self._get_edges()
        self.corners = self._get_corners()
