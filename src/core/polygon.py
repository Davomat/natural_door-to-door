from core.beam import Beam
from core.corner import Corner
from core.direction import Direction
from core.edge import Edge
from core.point import Point


class Polygon:
    """
    A class to represent a two-dimensional polygon.

    Args
    ----
    points : list[Point]
        The points that create the outer shell of the polygon.

    Attributes
    ----------
    points : list[Point]
        The points that stretch out the outer shell of the polygon.
    edges : list[Edge]
        The edges that are the outer shell of the polygon.
    corners : list[Corner]
        The corners of the outer shell.
    """

    def __init__(self, points: list[Point], is_room=True):
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
            if Edge(self.points[i % len(self)], self.points[i - 2]).contains_point(self.points[(i - 1) % len(self)]):
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
        return [Corner(self.edges[(i - 1) % len(self)], self.edges[i]) for i in range(len(self))]

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

    def get_virtual_polygon(self, nat_dist: float, sharp_angle: float) -> 'Polygon':
        """
        Calculates a new polygon inside the original if its counterclockwise (and outside otherwise),
        with the given natural distance to the original.

        The created polygon edges are parallel to the original ones with the given distance.
        The corner points may have a greater distance to its original corners respectively.
        """
        # initialize points for new polygon
        new_points = []

        # create points in every corner
        for corner in self.corners:

            # skip straight lines
            if 179. < corner.angle < 181.:
                continue

            # calculate parallel beams
            nat_dist_beam_1 = corner.e1.to_beam().nat_dist_beam(nat_dist)
            nat_dist_beam_2 = corner.e2.to_beam().nat_dist_beam(nat_dist)

            # normal corners
            if corner.angle < sharp_angle:
                new_points.append(Beam.intersection(nat_dist_beam_1, nat_dist_beam_2))

            # by definition sharp corners
            else:
                perpendicular_nat_dist_bisector = corner.bisector.perpendicular_nat_dist_beam(nat_dist)
                new_points.append(Beam.intersection(nat_dist_beam_1, perpendicular_nat_dist_bisector))
                new_points.append(Beam.intersection(nat_dist_beam_2, perpendicular_nat_dist_bisector))

        # return list of found points as polygon
        return Polygon(new_points, is_room=self._is_counterclockwise)

    def get_other_virtual_polygon(self, nat_dist: float, sharp_angle: float) -> 'Polygon':
        """
        Calculates a new polygon on the other side then `get_virtual_polygon`.
        """
        self._reverse()
        new_polygon = self.get_virtual_polygon(nat_dist, sharp_angle)
        self._reverse()
        return new_polygon

    def cuts_edge(self, other_edge: Edge) -> bool:
        """
        Checks if a given edge is cutting any of the polygons edges.

        The endpoints of the given other_edge may touch the polygon, this is not considered `cutting`.
        However, corners of the polygon may not touch the edge line.
        """
        # cutting other_edge with edge
        for self_edge in self.edges:
            if Edge.intersection(self_edge, other_edge):
                return True
        # cutting other_edge with point that is not also an end point of other_edge.
        for self_point in self.points:
            if self_point in other_edge.points:
                continue
            if other_edge.contains_point(self_point):
                return True
        # all clear
        return False

    def surrounds_or_hits_point(self, point: Point) -> bool:
        """
        Checks if a given point lies on or is inside of the polygon.
        """
        return self.surrounds_point(point) or self.hits_point(point)

    def hits_point(self, point: Point) -> bool:
        """
        Checks if a given point lies on the polygon.
        """
        for edge in self.edges:
            if edge.contains_point(point):
                return True
        return False

    def surrounds_point(self, point: Point) -> bool:
        """
        Checks if a given point is inside of the polygon.

        This is done by calculating how many edges and corners are cut by a random beam with the point as start.
        """
        # exclude point on edges
        if self.hits_point(point):
            return False
        # setup simple control beam in x-direction
        control_beam = Beam(point, Direction(1, 0))
        cut_counter = 0
        # check how many wall edges in one direction from the point get hit by the beam from the point
        cut_counter += self._count_cut_edges(control_beam)
        # check how many corners the beam cuts (not passes)
        cut_counter += self._count_cut_corners(control_beam)
        # if the amount is odd, the point is inside
        return cut_counter % 2 == 1

    def _count_cut_edges(self, beam: Beam) -> int:
        """
        Calculates how many edges of the polygon are cut by a beam.
        """
        edge_counter = 0
        for edge in self.edges:
            intersection = Beam.intersection(edge.to_beam(), beam)
            # intersection must exist, be on the right of the point, and be on the edge
            if intersection is not None \
                    and intersection.x > beam.pt.x \
                    and edge.contains_point(intersection):
                edge_counter += 1
        return edge_counter

    def _count_cut_corners(self, beam: Beam) -> int:
        """
        Calculates how many corners of the polygon are cut by a beam.

        To cut a corner, its edges must both lead upwards or downwards.
        A horizontal edge in between must be ignored.
        """
        corner_counter = 0
        last_edge_y_norm = self.corners[0].e1.get_edge_y_norm()
        for corner in self.corners:
            this_edge_y_norm = corner.e2.get_edge_y_norm()
            if this_edge_y_norm == 0:
                continue
            if corner.pt.x > beam.pt.x \
                    and beam.hits_point(corner.pt) \
                    and last_edge_y_norm == this_edge_y_norm:
                corner_counter += 1
            last_edge_y_norm = this_edge_y_norm
        return corner_counter

    @staticmethod
    def sample1() -> 'Polygon':
        """
        Returns a polygon with 10 corners looking like this:

        6 .____.____.____.____. 4
          |         5         |
          |                   L____. 2
          |                  3     |
        7 L____.____. 8            |
                     \\            |
                       \\ 9        |
                         |         |
                       0 L____.____| 1
        """
        return Polygon([
            Point(30.,  0.), Point(50., 0.), Point(50., 30.), Point(40., 30.), Point(40., 40.),
            Point(20., 40.), Point(0., 40.), Point(0.,  20.), Point(20., 20.), Point(30., 10.),
        ])

    @staticmethod
    def sample2() -> 'Polygon':
        """
        Returns a polygon with 16 edges/corners looking like this:

                 ._____.  ._____.
                 |     |  |     |
                 |  ___|  |     |
                 | |      |     |
        .________| |      |___. |
        |          L__________| |
        |                       |
        L_____.                 |
              |                 |
              L_________________|
        """
        return Polygon([
            Point(5.,   0.), Point(20.,  0.), Point(20., 20.), Point(15., 20.),
            Point(15., 10.), Point(18., 10.), Point(18.,  8.), Point(10.,  8.),
            Point(10., 15.), Point(13., 15.), Point(13., 20.), Point(8.,  20.),
            Point(8.,  10.), Point(0.,  10.), Point(0.,   4.), Point(5.,   4.),
        ])
