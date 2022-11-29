from typing import Optional

from core.point import Point
from core.direction import Direction


class Beam:
    """
    A class to represent a beam as a point with a direction.

    Args
    ----
    point : Point
        starting point of the beam
    direction : Direction
        direction of the beam

    Attributes
    ----------
    pt : Point
        starting point of the beam
    dir : Direction
        direction of the beam
    """

    def __init__(self, point: Point, direction: Direction):
        self.pt: Point = point
        self.dir: Direction = direction

    def __repr__(self):
        return repr(self.pt) + repr(self.dir)

    def __eq__(self, other):
        return self.pt == other.pt and self.dir == other.dir

    def nat_dist_beam(self, nat_dist: float) -> 'Beam':
        """
        Returns a new Beam instance with the same direction but nat_dist away (to the left) of the given one.
        """
        return Beam(self.pt + self.dir.perpendicular().naturalized(nat_dist).to_point(), self.dir)

    def perpendicular_nat_dist_beam(self, nat_dist: float) -> 'Beam':
        """
        Calculates the perpendicular beam to the given beam.
        The new beam starts on the given one with a distance of nat_dist to its the start.
        """
        nat_vec = self.dir.naturalized(nat_dist)
        new_pt = self.pt + nat_vec.to_point()
        new_dir = self.dir.perpendicular()
        return Beam(new_pt, new_dir)

    @staticmethod
    def intersection(b1: 'Beam', b2: 'Beam') -> Optional[Point]:
        """
        Returns the intersection point of two given beams.

        Returns None if no distinct intersection can be found.
        """
        # Check if beams are parallel (have the same direction vector)
        if b1.dir.normalized() == b2.dir.normalized():
            return None

        # new_beam = beam1.pt + r1 * beam1.dir
        r1: float = ((b2.pt.x - b1.pt.x) * b2.dir.y + (b1.pt.y - b2.pt.y) * b2.dir.x) / \
                    (b1.dir.x * b2.dir.y - b1.dir.y * b2.dir.x)
        return Point(b1.pt.x + r1 * b1.dir.x, b1.pt.y + r1 * b1.dir.y)
