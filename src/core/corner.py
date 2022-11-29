from core.beam import Beam
from core.point import Point
from core.edge import Edge


class Corner:
    """
    A class to represent two adjacent edges of a polygon.

    Args
    ----------
    e1 : Edge
        first edge counterclockwise
    e2 : Edge
        second edge counterclockwise

    Attributes
    ----------
    e1 : Edge
        first edge counterclockwise
    e2 : Edge
        second edge counterclockwise
    pt : Point
        the point of the corner that connects both edges
    """

    def __init__(self, e1: Edge, e2: Edge):
        self.e1: Edge = e1
        self.e2: Edge = e2
        self.pt: Point = e1.p2

    def __repr__(self):
        return f"{self.e1.p1} - {self.pt} - {self.e2.p2}"

    @property
    def edges(self):
        """
        Returns the edges defining the corner as a tuple.
        """
        return [self.e1, self.e2]

    @property
    def angle(self) -> float:
        """
        Returns the angle between two vectors in degree.
        """
        return (self.e1.dir.angle + 180 - self.e2.dir.angle) % 360

    @property
    def bisector(self) -> Beam:
        """
        Calculates the bisector of the corner and returns it as beam object.
        """
        # get the normalized edge directions
        d1 = self.e1.dir.normalized()
        d2 = self.e2.dir.normalized()

        # set bisector direction according to angle
        if d1 == d2:  # corner angle is about 180°
            new_dir = d1.perpendicular()
        elif self.angle > 180:
            new_dir = d1 - d2
        else:  # self.angle < 180:
            new_dir = d2 - d1

        # return new beam
        return Beam(self.pt, new_dir)
