from pat.gen import result_polygon
from pat.geo.polygon import Polygon


def almost_sierpinski(triangle: Polygon, abs_spacing: float, rel_spacing: float, depth: int):
    points = triangle.points
    assert len(points) == 3
    if depth == 0:
        return

    def space(middle, center):
        towards_center = center-middle
        absolute = towards_center.normalized()*abs_spacing
        if absolute.sqnorm() >= 2*towards_center.sqnorm():
            relative = towards_center*rel_spacing
            return middle + relative
        else:
            return middle + absolute

    center = (points[0] + points[1] + points[2])/3
    middles = list(triangle.sides_middles())
    vertices = [space(m, center) for m in middles]
    yield result_polygon(vertices)  # triangle central

    for k in range(3):
        sub_triangle = result_polygon([points[k], middles[k], middles[(k + 2) % 3]])
        yield from almost_sierpinski(sub_triangle, abs_spacing, rel_spacing, depth-1)
