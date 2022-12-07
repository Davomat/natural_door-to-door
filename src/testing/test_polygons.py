from core.point import Point
from core.polygon import Polygon

from shapely import geometry


def polygon_inner_outer(polygon: Polygon, natural_distance: float, sharp_angle: float):
    print('AusgangsPolygon:', polygon, ' - Länge:', len(polygon))
    inner_polygon = polygon.virtual_polygon(natural_distance, sharp_angle)
    print('Inneres Polygon:', inner_polygon, ' - Länge:', len(inner_polygon))
    outer_polygon = polygon.other_virtual_polygon(natural_distance, sharp_angle)
    print('Äußeres Polygon:', outer_polygon, ' - Länge:', len(outer_polygon))


def polygon_inner_outer1(natural_distance: float, sharp_angle: float):
    polygon_inner_outer(Polygon.sample1(), natural_distance, sharp_angle)


def polygon_inner_outer2(natural_distance: float, sharp_angle: float):
    polygon_inner_outer(Polygon.sample2(), natural_distance, sharp_angle)


def polygon_contains():
    print('\n' + '--- Testing correlations between points and polygons with own code and shapely ---' + '\n')
    polygon = Polygon.sample1()
    shapely_polygon = geometry.Polygon([(p.x, p.y) for p in polygon.points])

    points_on_outline = [Point(30, 10), Point(30, 0), Point(50, 0), Point(50, 30), Point(40, 30),
                         Point(40, 40), Point(20, 40), Point(0, 40), Point(0, 20), Point(20, 20),
                         Point(30, 5), Point(40, 0), Point(50, 10), Point(45, 30), Point(40, 35),
                         Point(30, 40), Point(0, 30), Point(10, 20), Point(25, 15)]
    shapely_points_on_outline = [geometry.Point((p.x, p.y)) for p in points_on_outline]
    print('Test points on outline for outline:\n'
          'should be:', [True] * len(points_on_outline), '\n'
          '...and is:',
          [polygon.hits_point(p) for p in points_on_outline], '\n'
          '..shapely:',
          [shapely_polygon.intersects(p) and not shapely_polygon.contains(p) for p in shapely_points_on_outline])
    print('Test points on outline for inside:\n'
          'should be:', [False] * len(points_on_outline), '\n'
          '...and is:',
          [polygon.surrounds_point(p) for p in points_on_outline], '\n'
          '..shapely:',
          [shapely_polygon.contains(p) for p in shapely_points_on_outline], '\n')

    points_inside = [Point(30, 11), Point(32, 5), Point(40, 20), Point(20, 30), Point(40, 20),
                     Point(40, 10), Point(20, 30), Point(1, 30), Point(10, 21), Point(20, 30),
                     Point(30, 17), Point(41, 1), Point(49, 1), Point(49, 29), Point(39, 29),
                     Point(21, 21)]
    shapely_points_inside = [geometry.Point((p.x, p.y)) for p in points_inside]
    print('Test points inside for outline:\n'
          'should be:', [False] * len(points_inside), '\n'
          '...and is:',
          [polygon.hits_point(p) for p in points_inside], '\n'
          '..shapely:',
          [shapely_polygon.intersects(p) and not shapely_polygon.contains(p) for p in shapely_points_inside])
    print('Test points inside for inside:\n'
          'should be:', [True] * len(points_inside), '\n'
          '...and is:',
          [polygon.surrounds_point(p) for p in points_inside], '\n'
          '..shapely:',
          [shapely_polygon.contains(p) for p in shapely_points_inside], '\n')

    points_outside = [Point(28, 10), Point(30, -1), Point(51, 0), Point(150, 30),
                      Point(41, 41), Point(20, 50), Point(-1, 40), Point(0, 10), Point(20, 19),
                      Point(15, 5), Point(40, -0.1), Point(150, -10), Point(-1, 30)]
    shapely_points_outside = [geometry.Point((p.x, p.y)) for p in points_outside]
    print('Test points outside for outline:\n'
          'should be:', [False] * len(points_outside), '\n'
          '...and is:',
          [polygon.hits_point(p) for p in points_outside], '\n'
          '..shapely:',
          [shapely_polygon.intersects(p) and not shapely_polygon.contains(p) for p in shapely_points_outside])
    print('Test points outside for inside:\n'
          'should be:', [False] * len(points_outside), '\n'
          '...and is:',
          [polygon.surrounds_point(p) for p in points_outside], '\n'
          '..shapely:',
          [shapely_polygon.contains(p) for p in shapely_points_outside], '\n')

    polygon = Polygon([Point(0, 0), Point(10, 0), Point(10, 10), Point(5, 5), Point(0, 10)])
    shapely_polygon = geometry.Polygon([(p.x, p.y) for p in polygon.points])

    points = [Point(0, 0), Point(10, 0), Point(10, 10), Point(5, 5), Point(0, 10),
              Point(5, 0), Point(10, 5), Point(7.5, 7.5), Point(2.5, 7.5), Point(0, 5),
              Point(5, 1), Point(2, 5), Point(7.5, 1.5), Point(2.5, 2.5), Point(1, 7),
              Point(-1, 0), Point(-10, 10), Point(-5, 5), Point(-2.5, 7.5), Point(0, 15)]
    shapely_points = [geometry.Point((p.x, p.y)) for p in points]
    print('Test mixed points for outline:\n'
          'should be: [True, True, True, True, True, True, True, True, True, True,'
          ' False, False, False, False, False, False, False, False, False, False]', '\n'
          '...and is:',
          [polygon.hits_point(p) for p in points], '\n'
          '..shapely:',
          [shapely_polygon.intersects(p) and not shapely_polygon.contains(p) for p in shapely_points])
    print('Test mixed points for inside:\n'
          'should be: [False, False, False, False, False, False, False, False, False, False,'
          ' True, True, True, True, True, False, False, False, False, False]', '\n'
          '...and is:',
          [polygon.surrounds_point(p) for p in points], '\n'
          '..shapely:',
          [shapely_polygon.contains(p) for p in shapely_points], '\n')
