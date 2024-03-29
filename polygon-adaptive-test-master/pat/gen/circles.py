from math import cos, sin, pi

from pat.gen import result_polygon
from pat.geo.vector import Vector


def pixelized_circle(center_x: float, center_y: float, r: float, n: int):
    points = [None]*n
    for k in range(n):
        theta = (k/n)*(2*pi)
        x = center_x - r*cos(theta)
        y = center_y - r*sin(theta)
        points[k] = Vector(x,y)
    return result_polygon(points)

def aligned_circles(x0: float, y0: float, radius: float, shift_x: float, shift_y: float, n_points: int, number: int):
    assert max(shift_x, shift_y) > 2*radius
    x, y, r = x0, y0, radius
    for n in range(number):
        yield pixelized_circle(x, y, r, n_points)
        x += shift_x
        y += shift_y

def nested_circles(center_x: float, center_y: float, r0: float, spacing: float, n_points: int, depth: int):
    r = r0
    for n in range(depth):
        yield pixelized_circle(center_x, center_y, r, n_points)
        r -= spacing
