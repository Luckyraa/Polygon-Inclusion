from geo.polygon import Polygon,Point

import math

def separate_polygons_with_line(polygones, line, type):
    """
    etant donnee une ligne et son type vertical ou horizontal,
    classe les polygones en 3 categories, dedans, dehors ou au milieu si la ligne croise le polygone
    on choisit par convention que le dedans est la zone de x ou de y la plus faible selon le type de la ligne
    """
    if type == 'vertical':
        polygon_in_zone = lambda pol, line: pol.max_x <= line
        polygon_in_line = lambda pol, line: pol.min_x < line and pol.max_x > line  # in theory the second part is not needed since wz already know that the pol isn't in zone
    elif type == 'horizontal':
        polygon_in_zone = lambda pol, line: pol.max_y <= line
        polygon_in_line = lambda pol, line: pol.min_y < line and pol.max_y > line  # in theory the second part is not needed since wz already know that the pol isn't in zone  

    in_zone = set([])
    in_milieu = set([])
    outside = set([])
    for polygon in polygones:
        if polygon_in_zone(polygon, line):
            in_zone.add(polygon)
        else:
            outside.add(polygon)

            if polygon_in_line(polygon, line):
                in_milieu.add(polygon)

    return in_zone, in_milieu, outside


def separate_polygons_to_zones(polygones, num_horisontal_lines, num_vertical_lines):
    """
    utilise separate_polygons_with_line pour creer l'ensemble du quadrillage de la fenêtre en zones
    la classe Polygon a ete modifiee en consequence pour stocker la zone a laquelle chaque polygone appartient
    """
    vertical_line_delta   = ( (Polygon.ABS_MAX_X - Polygon.ABS_MIN_X)//(num_vertical_lines + 1) ) +1
    horizontal_line_delta = ( (Polygon.ABS_MAX_Y - Polygon.ABS_MIN_Y)//(num_horisontal_lines + 1) ) +1
    vertical_zones          = []
    vertical_zones_milieu   = []
    horizontal_zones        = []
    horizontal_zones_milieu = []

    le_rest = polygones
    for i in range(num_vertical_lines + 1):
        new_zone, zone_milieu, le_rest = separate_polygons_with_line(le_rest, Polygon.ABS_MIN_X + vertical_line_delta*(i+1), type='vertical')
        vertical_zones.append(new_zone)
        vertical_zones_milieu.append(zone_milieu)

    le_rest = polygones
    for i in range(num_horisontal_lines + 1):
        new_zone, zone_milieu, le_rest = separate_polygons_with_line(le_rest, Polygon.ABS_MIN_Y + horizontal_line_delta*(i+1), type='horizontal')
        horizontal_zones.append(new_zone)
        horizontal_zones_milieu.append(zone_milieu)

    for vertical_zone, vertical_milieu in zip(vertical_zones, vertical_zones_milieu):
        for horizontal_zone, horizontal_milieu in zip(horizontal_zones, horizontal_zones_milieu):
            new_zone = set.intersection(vertical_zone, horizontal_zone) | horizontal_milieu | vertical_milieu

            for pol in new_zone:
                pol.zone = new_zone



