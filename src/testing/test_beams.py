from core.beam import Beam
from core.direction import Direction
from core.point import Point


def sample_beam_1() -> Beam:
    return Beam(Point(0., 0.), Direction(1, 1))


def sample_beam_2() -> Beam:
    return Beam(Point(5., 2.), Direction(1, 0))


def sample_beam_3() -> Beam:
    return Beam(Point(4., 0.), Direction(0., 7.))


def sample_intersection_1(nat_dist: float):
    b1 = sample_beam_1()
    b2 = sample_beam_2()
    print('Beam 1:', str(b1))
    print('Beam 2:', str(b2))
    print('Intersection:', Beam.intersection(b1, b2))

    b1_nat = b1.nat_dist_beam(nat_dist)
    b2_nat = b2.nat_dist_beam(nat_dist)
    print('nat-Dist-Beam 1:', str(b1_nat))
    print('nat-Dist-Beam 2:', str(b2_nat))
    print('Intersection:', Beam.intersection(b1_nat, b2_nat), '\n')


def sample_intersection_2(nat_dist: float):
    b1 = sample_beam_2()
    b2 = sample_beam_3()
    print('Beam 1:', str(b1))
    print('Beam 2:', str(b2))
    print('Intersection:', Beam.intersection(b1, b2))

    b1_nat = b1.nat_dist_beam(nat_dist)
    b2_nat = b2.nat_dist_beam(nat_dist)
    print('nat-Dist-Beam 1:', str(b1_nat))
    print('nat-Dist-Beam 2:', str(b2_nat))
    print('Intersection:', Beam.intersection(b1_nat, b2_nat), '\n')
