from core.polygon import Polygon
from core.room import Room


def test_room_1(natural_distance: float, sharp_angle: float, print_for_tex=False):
    room = Room.sample()
    room.find_paths(natural_distance, sharp_angle)
    print()
    print('Originale Raumbegrenzung (', len(room.boundary), '):\t', room.boundary, sep='')
    print('Virtuelle Raumbegrenzung (', len(room.virtual_boundary), '):\t', room.virtual_boundary, sep='')
    print()
    print('Originale Barrieren (', len(room.barriers), '):\t', room.barriers, sep='')
    print('Virtuelle Barrieren (', len(room.virtual_barriers), '):\t', room.virtual_barriers, sep='')
    print()
    print('Originale Türen (', len(room.doors), '):\t', room.doors, sep='')
    print('Virtuelle Türen (', len(room.virtual_doors), '):\t', room.virtual_doors, sep='')
    print()
    print('Navigation Points (', len(room.nav_points), '):\t', room.nav_points, sep='')
    print('Navigation Paths (', len(room.nav_edges), '): \t', room.nav_edges, sep='')

    if print_for_tex:
        print_for_latex(room)


def print_for_latex(room: Room):
    # some space
    print('\n')

    # walls
    for polygon in [room.boundary] + room.barriers:
        print(f'\\draw[ultra thick] ', end='')
        for p in polygon.points:
            print(f'({round(p.x, 4)},{round(p.y, 4)}) -- ', end='')
        print(f'({round(polygon.points[0].x, 4)},{round(polygon.points[0].y, 4)});')

    # navigation nodes
    for d in room.doors:
        print(f'\\node[circle, draw, thick, scale=1.0] () at ({round(d.x, 4)},{round(d.y, 4)})', '{};')
    for p in room.nav_points:
        print(f'\\node[circle, draw, thick, scale=0.5] () at ({round(p.x,4)},{round(p.y,4)})', '{};')

    # navigation paths
    for e in room.nav_edges:
        print(f'\\draw[blue] ({round(e.p1.x,4)},{round(e.p1.y,4)}) -- ({round(e.p2.x,4)},{round(e.p2.y,4)});')
