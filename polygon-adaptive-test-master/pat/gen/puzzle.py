from pat.gen import result_polygon
from pat.geo.polygon import Polygon
from pat.geo.vector import Vector

PUZZLE_PIECE_POLYGONS = [
    Polygon([
        Vector(0.21, 0.19),
        Vector(2.69, 1.87),
        Vector(2.19, -1.91),
        Vector(5.0, -6.0),
        Vector(-1.0, -10.0),
        Vector(1.0, -6.0),
        Vector(-3.0, -7.0),
        Vector(0.37, -4.57),
        Vector(0.19, -2.57),
        Vector(2.27, -3.57),
        Vector(2.33, -2.89),
    ]),
    Polygon([
        Vector(-3.0, -2.0),
        Vector(0.0, -0.0),
        Vector(2.0, -3.0),
        Vector(0.0, -2.0),
        Vector(0.0, -4.0),
    ]),
    Polygon([
        Vector(-3.05, -7.43),
        Vector(0.63, -6.25),
        Vector(-0.85, -9.43),
        Vector(-1.25, -9.79),
    ]),
    Polygon([
        Vector(-3.33, -6.81),
        Vector(0.0, -4.57),
        Vector(-3.21, -2.21),
    ])
]

def puzzle_piece(shift):
    for p in PUZZLE_PIECE_POLYGONS:
        yield result_polygon(p.shifted_points(shift))

def puzzle(width, height, spacing):
    v = Vector(6.15, 4.1)*spacing
    w = Vector(-4.39, 6.49)*spacing
    for i in range(width):
        for j in range(height):
            yield from puzzle_piece(v*i + w*j)
