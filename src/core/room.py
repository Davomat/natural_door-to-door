from typing import Optional

from core.beam import Beam
from core.edge import Edge
from core.point import Point
from core.polygon import Polygon
from core.std_vals import *


class Room:
    """
    A class representing a room containing walls, doors, and .

    Args
    ----
    boundary : Polygon
        Defines the outer polygon of the Room area.
    barriers : list[Polygon]
        The obstacles inside the room that must be bypassed.
    doors : list[Point]
        The doors that connect the room to other rooms or areas.

    Attributes
    ----------
    boundary : Polygon
        Defines the outer polygon of the Room area.
    virtual_boundary : Polygon
        Defines the virtual outer polygon inside the real outer polygon, having the natural distance to it.
    barriers : list[Polygon]
        The obstacles inside the room that must be bypassed.
    virtual_barriers : list[Polygon]
        The virtual polygons outside the real obstacle polygons, having the natural distance to them.
    doors : list[Point]
        The doors that connect the real room to other rooms or areas.
    virtual_doors : list[Point]
        The virtual doors on the virtual polygons.
    nav_points : list[Point]
        The points used for calculating the navigation paths.
    nav_edges : list[Edge]
        The edges defining routes for navigation.
    """

    def __init__(self, boundary: Polygon, barriers: list[Polygon], doors: list[Point]):
        self.boundary: Polygon = boundary
        self.barriers: list[Polygon] = barriers
        self.doors: list[Point] = doors
        # prepare other members
        self.virtual_boundary: Optional[Polygon] = None
        self.virtual_barriers: list[Polygon] = []
        self.virtual_doors: list[Point] = []
        self.nav_points: list[Point] = []
        self.nav_edges: list[Edge] = []

    def __repr__(self) -> str:
        return f"Room:\nboundary: {repr(self.boundary)}\nbarriers: {repr(self.barriers)}\ndoors: {repr(self.doors)}"

    def _set_virtual_boundary(self, nat_dist: float, sharp_angle: float):
        """
        Calculates the rooms virtual inner boundary polygon according to the given values.
        """
        self.virtual_boundary = self.boundary.get_virtual_polygon(nat_dist, sharp_angle)

    def _set_virtual_barriers(self, nat_dist: float, sharp_angle: float):
        """
        Calculates the rooms virtual outer barrier polygons according to the given values.
        """
        self.virtual_barriers = [barrier.get_virtual_polygon(nat_dist, sharp_angle) for barrier in self.barriers]

    def _set_virtual_doors(self, nat_dist: float):
        """
        Calculates the rooms virtual doors on the virtual polygons.
        """
        # TODO find mistake (first door in room sample)
        for door in self.doors:
            # find the edge the door is positioned at
            door_edge = self._corresponding_edge(door)
            print(door, 'auf', door_edge)
            # take the edge's beam starting from the door - the virtual door is the start point of the nat-dist-beam
            virtual_door = Beam(door, door_edge.dir).nat_dist_beam(nat_dist).pt
            # add to list
            self.virtual_doors.append(virtual_door)

    def _virtualize(self, nat_dist: float, sharp_angle: float):
        """
        Calculates the rooms virtual polygons for the outer walls and inner barriers according to the given values.
        """
        self._set_virtual_boundary(nat_dist, sharp_angle)
        self._set_virtual_barriers(nat_dist, sharp_angle)
        self._set_virtual_doors(nat_dist)

    def _corresponding_edge(self, pt: Point) -> Edge:
        """
        Finds the edge that corresponds to a door.
        """
        # check outer room
        for edge in self.boundary.edges:
            if edge.contains_point(pt, tolerance=door_tolerance):
                return edge
        # check barriers (that can also be little rooms inside a big one)
        for barrier in self.barriers:
            for edge in barrier.edges:
                if edge.contains_point(pt, tolerance=door_tolerance):
                    return edge
        # point belongs to no edge of the room
        raise RuntimeError(f'Point {pt} does not belong to room {self}')

    def _collect_nav_points(self):
        """
        Collects all possible points for the navigation through the room.
        """
        # add inner corners from outer shell
        for corner in self.virtual_boundary.corners:
            if corner.angle > 180:
                self.nav_points.append(corner.pt)
        # add outer corners from inner barriers
        for barrier in self.virtual_barriers:
            for corner in barrier.corners:
                if corner.angle > 180:
                    self.nav_points.append(corner.pt)
        # add points in front of doors
        for door in self.virtual_doors:
            self.nav_points.append(door)

    def _collect_nav_edges(self):
        """
        Connects all pairwise combinations of the nav_points if the connection is valid.
        A valid connection lies completely in the virtual room and does not cut any edge.
        """
        # TODO write

    def find_paths(self, nat_dist: float, sharp_angle: float) -> list[Edge]:
        """
        Calculates the navigation mesh (path graph) for the room according to the given values.
        """
        # calculate virtual polygons
        self._virtualize(nat_dist, sharp_angle)
        # collect navigation points
        self._collect_nav_points()
        # connect all points if valid
        self._collect_nav_edges()
        # return paths
        return self.nav_edges

    @staticmethod
    def sample() -> 'Room':
        """
        Returns a room with a barrier inside, looking like this:
        .____.____.____.____.
        |    .____.         o
        o    L_o__|         L____.
        |                        |
        L____.____.    .____.    |
                   \\   \\  |    o
                     \\   \\|    |
                       |         |
                       L____o____|
        """
        boundary = Polygon.sample1()
        barriers = [Polygon([Point(10., 30.), Point(20., 30.), Point(20., 35.), Point(10., 35.)], False),
                    Polygon([Point(30., 20.), Point(40., 20.), Point(40., 10.)], False)]
        doors = [Point(0., 30.), Point(15., 30.), Point(40., 0.), Point(40., 35.), Point(50., 15.)]

        return Room(boundary, barriers, doors)
