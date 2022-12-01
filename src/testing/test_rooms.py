from core.room import Room


def test_room_1(natural_distance: float, sharp_angle: float):
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
