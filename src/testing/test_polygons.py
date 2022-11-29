from core.polygon import Polygon


def polygon_inner_outer(polygon: Polygon, natural_distance: float):
    print('AusgangsPolygon:', polygon, ' - Länge:', len(polygon))
    inner_polygon = polygon.get_inner_polygon(natural_distance)
    print('Inneres Polygon:', inner_polygon, ' - Länge:', len(inner_polygon))
    outer_polygon: Polygon = polygon.get_outer_polygon(natural_distance)
    print('Äußeres Polygon:', outer_polygon, ' - Länge:', len(outer_polygon))


def polygon_inner_outer1(natural_distance: float):
    polygon_inner_outer(Polygon.sample1(), natural_distance)


def polygon_inner_outer2(natural_distance: float):
    polygon_inner_outer(Polygon.sample2(), natural_distance)
