from core.polygon import Polygon


def polygon_inner_outer(polygon: Polygon, natural_distance: float, sharp_angle: float):
    print('AusgangsPolygon:', polygon, ' - Länge:', len(polygon))
    inner_polygon = polygon.get_virtual_polygon(natural_distance, sharp_angle)
    print('Inneres Polygon:', inner_polygon, ' - Länge:', len(inner_polygon))
    outer_polygon = polygon.get_other_virtual_polygon(natural_distance, sharp_angle)
    print('Äußeres Polygon:', outer_polygon, ' - Länge:', len(outer_polygon))


def polygon_inner_outer1(natural_distance: float, sharp_angle: float):
    polygon_inner_outer(Polygon.sample1(), natural_distance, sharp_angle)


def polygon_inner_outer2(natural_distance: float, sharp_angle: float):
    polygon_inner_outer(Polygon.sample2(), natural_distance, sharp_angle)
