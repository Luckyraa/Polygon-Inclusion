from typing import Iterable, Tuple, List

from pat import couples
from .quadrant import Quadrant
from .vector import Vector


class Polygon:
    __slots__ = ["points", "parent"]

    def __init__(self, points: List[Vector], parent=None):
        self.points = points
        self.parent = parent

    def segments(self) -> Iterable[Tuple[Vector, Vector]]:
        """Iterates on the polygon's segments, in a sensible order."""
        return couples(self.points)

    def sides_middles(self) -> Iterable[Vector]:
        """Iterates through the middles of the sides of the polygon."""
        return ((s[0] + s[1]) / 2 for s in self.segments())

    def shifted_points(self, vec):
        return [p + vec for p in self.points]

    def bounding_quadrant(self):
        box = Quadrant.empty_quadrant(2)
        for point in self.points:
            box.add_point(point)
        return box

    def svg_content(self, color):
        """
        svg for tycat.
        """
        svg_coordinates = (
            "{},{}".format(*p)
            for p in self.points
        )
        svg_formatted = " ".join(svg_coordinates)
        return '<polygon points="{}" fill="{}" stroke="{}" fill-opacity="0.3"/>'.format(svg_formatted, color, color)

    def __str__(self):
        points_str = ",\n".join(str(p) for p in self.points)
        return f"Polygon([{points_str}])"
