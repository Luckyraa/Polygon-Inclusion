import os

from pat import couples
from pat.geo.polygon import Polygon

DEOPT_FACTOR = int(os.getenv("DEOPT_FACTOR", 1))

def deoptimize(points, deopt_factor):
    """
    Deoptimizes a polygon by adding unnecessary vertices
    """
    result = []
    k_range = range(deopt_factor)
    for a,b in couples(points):
        step = (b-a)/deopt_factor
        result.extend([a + step*k for k in k_range])
    return result

def result_polygon(points, known_parent=None):
    return Polygon(deoptimize(points, DEOPT_FACTOR), known_parent)

def tmp_polygon(points):
    return Polygon(points)
