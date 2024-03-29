"""
polygons.
"""
from geo.point import Point
from geo.segment import Segment
from geo.quadrant import Quadrant
from itertools import islice, cycle

def couples(iterable):
    """
    iterate on all couples of given iterable.
    this will wrap around last element.
    """
    return zip(iterable, islice(cycle(iterable), 1, None))

class Polygon:
    """
    a polygon is an ordered set of points.

    for example:

    - create a triangle:

    triangle = Polygon([Point([0, 0]), Point([1, 1]), Point([2, 0])])

    - loop on all segments in a polygon:

    for segment in polygon.segments():
        ....

    """
    ABS_MAX_X = -float("inf")
    ABS_MAX_Y = -float("inf")
    ABS_MIN_X = float("inf")
    ABS_MIN_Y = float("inf")
    INDEX = 0

    def __init__(self, points):
        assert len(points) > 2
        self.points = points

        self.min_x = min([point.coordinates[0] for point in self.points])
        self.max_x = max([point.coordinates[0] for point in self.points])
        self.min_y = min([point.coordinates[1] for point in self.points])
        self.max_y = max([point.coordinates[1] for point in self.points])

        Polygon.ABS_MAX_X = max(Polygon.ABS_MAX_X, self.max_x)
        Polygon.ABS_MAX_Y = max(Polygon.ABS_MAX_Y, self.max_y)
        Polygon.ABS_MIN_X = min(Polygon.ABS_MIN_X, self.min_x)
        Polygon.ABS_MIN_Y = min(Polygon.ABS_MIN_Y, self.min_y)

        self.zone = []
        self.hash = id(self)

        self.index = Polygon.INDEX   # saves polygone index
        Polygon.INDEX += 1

    @classmethod
    def square(cls, start_x, start_y, side):
        """
        create a square, horizontally aligned.
        used in test scripts as a quick way to get polygons.
        """
        starting_point = Point([start_x, start_y])
        points = [
            Point([0.0, 0.0]),
            Point([side, 0.0]),
            Point([side, side]),
            Point([0.0, side]),
        ]
        points = [p + starting_point for p in points]
        square_polygon = cls(points)
        return square_polygon

    def segments(self):
        """
        iterate through all segments.
        """
        return map(Segment, couples(self.points))

    def area(self):
        """
        return polygon area. can be positive or negative, depending on
        orientation.
        """
        return sum(p1.cross_product(p2)
                   for p1, p2 in couples(self.points)) / 2

    def is_oriented_clockwise(self):
        """
        clockwise being defined respectively to svg displayed, return
        true if polygon is oriented clockwise.
        """
        area = self.area()
        return area > 0

    def orient(self, clockwise=True):
        """
        orient polygon with given orientation
        """
        if self.is_oriented_clockwise() != clockwise:
            return Polygon(self.points[::-1])
        else:
            return self

    def bounding_quadrant(self):
        """
        min quadrant containing polygon.
        """
        box = Quadrant.empty_quadrant(2)
        for point in self.points:
            box.add_point(point)
        return box

    def svg_content(self):
        """
        svg for tycat.
        """
        svg_coordinates = (
            "{},{}".format(*p.coordinates)
            for p in self.points
        )
        svg_formatted = " ".join(svg_coordinates)
        return '<polygon points="{}" fill="none"/>'.format(svg_formatted)

    def __str__(self):
        points = ",\n".join(str(p) for p in self.points)
        return "Polygon([" + points + "])\n"
    
    def __eq__(self, other):
        '''no two polygones are the same'''
        return self is other
    
    def __hash__(self) -> int:
        return self.hash
