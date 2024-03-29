from pat.gen import result_polygon
from pat.geo.vector import Vector


def square(start_x, start_y, side):
    """
    create a square, horizontally aligned.
    used in test scripts as a quick way to get polygons.
    """
    starting_point = Vector(start_x, start_y)
    points = [
        Vector(0.0, 0.0),
        Vector(side, 0.0),
        Vector(side, side),
        Vector(0.0, side)
    ]
    points = [p + starting_point for p in points]
    return result_polygon(points)

def aligned_squares(x0: float, y0: float, side: float, shift_x: float, shift_y: float, number: int):
    assert max(shift_x, shift_y) > side
    x,y,s = x0,y0,side
    for n in range(number):
        yield square(x,y,s)
        x += shift_x
        y += shift_y

def nested_squares(x0: float, y0: float, side0: float, spacing: float, depth: int):
    x,y,s = x0,y0,side0
    for n in range(depth):
        yield square(x,y,s)
        x += spacing/2
        y += spacing/2
        s -= spacing

def fake_square(x, y, side, thickness):
    starting_point = Vector(x, y)
    points = [
        Vector(0.0, 0.0),
        Vector(0.0, side),
        Vector(side, side),
        Vector(side, 0.0),
        Vector(side - thickness, 0.0),
        Vector(side - thickness, side - thickness),
        Vector(thickness, side - thickness),
        Vector(thickness, 0.0)
    ]
    points = [p + starting_point for p in points]
    return result_polygon(points)


def fake_nested_squares(x0, y0, depth):
    spacing = 1
    for i in range(2*depth, 0, -(2*spacing)):
        yield fake_square(x0, y0, i, spacing/2)
        x0 += spacing
        y0 += spacing