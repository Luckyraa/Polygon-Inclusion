from math import cos, sin, pi

from pat.gen import result_polygon
from pat.geo.vector import Vector

SIDE_DIVIDE_FACTOR = 3.1

def hexagon(centre, cote):
    """
    Renvoie 6 points ayant pour coordonnées ceux
    de l'hexagone de centre centre et de coté de longueur cote
    :author: Robin Lamy
    """
    points = []
    for i in range(6):
        points.append(Vector(centre.x + cote * cos(i * pi / 3), centre.y + cote * sin(i * pi / 3)))
    return points

def recursive_hexagons(depth, center, side):
    yield result_polygon(hexagon(center, side))
    if depth > 1:
        h = hexagon(center, side*2)
        next_side = side / SIDE_DIVIDE_FACTOR
        for vertex in h:
            yield from recursive_hexagons(depth-1, vertex, next_side)
