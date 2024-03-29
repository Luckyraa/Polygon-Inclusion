import sys

from pat.gen import result_polygon
from pat.geo.polygon import Polygon
from pat.geo.vector import Vector

def square_fractals(n):
    sys.setrecursionlimit(90000)
    carre = Polygon([Vector(0,0), Vector(500,0), Vector(500,500), Vector(0,500)])
    yield from recurse_squares(carre, n, 1)
    yield carre

def recurse_squares(carre, n, pas):
    """
    Carrés imbriqués récursivement.
    :author: Alexandre Wendling
    """
    quadrant = carre.bounding_quadrant()
    zone = [[quadrant.min_coordinates[0], quadrant.min_coordinates[1]], [quadrant.max_coordinates[0], quadrant.max_coordinates[1]]]
    vec_milieu = [(quadrant.min_coordinates[0]+quadrant.max_coordinates[0])/2, (quadrant.min_coordinates[1]+quadrant.max_coordinates[1])/2]
    if n == 1:
        return
    else:
        carre_1 = result_polygon([
            Vector(zone[0][0]+pas,zone[0][1]+pas),
            Vector(zone[0][0]+pas,vec_milieu[1]-pas),
            Vector(vec_milieu[0]-pas,vec_milieu[1]-pas),
            Vector(vec_milieu[0]-pas,zone[0][1]+pas)
        ])
        carre_2 = result_polygon([
            Vector(zone[0][0]+pas,vec_milieu[1]+pas),
            Vector(zone[0][0]+pas,zone[1][1]-pas),
            Vector(vec_milieu[0]-pas,zone[1][1]-pas),
            Vector(vec_milieu[0]-pas,vec_milieu[1]+pas)
        ])
        carre_3 = result_polygon([
            Vector(vec_milieu[0]+pas,vec_milieu[1]+pas),
            Vector(vec_milieu[0]+pas,zone[1][1]-pas),
            Vector(zone[1][0]-pas,zone[1][1]-pas),
            Vector(zone[1][0]-pas,vec_milieu[1]+pas)
        ])
        carre_4 = result_polygon([
            Vector(vec_milieu[0]+pas,zone[0][1]+pas),
            Vector(vec_milieu[0]+pas,vec_milieu[1]-pas),
            Vector(zone[1][0]-pas,vec_milieu[1]-pas),
            Vector(zone[1][0]-pas,zone[0][1]+pas)
        ])
        yield carre_1
        yield carre_2
        yield carre_3
        yield carre_4
        yield from recurse_squares(carre_1, n-1, pas)
        yield from recurse_squares(carre_2, n-1, pas)
        yield from recurse_squares(carre_3, n-1, pas)
        yield from recurse_squares(carre_4, n-1, pas)