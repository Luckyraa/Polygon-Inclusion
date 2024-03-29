from math import pi
from geo.point import Point
from geo.segment import Segment
from geo.polygon import Polygon
import sys
from tycat import read_instance

def intersect(s1, s2):
    """
    calcule le point d'intersection de s1 et s2
    renvoie true et le point si l'intersection existe
    false, None sinon
    si s1 est dans s2 ou inverse, renvoie False,None
    """
    x1,y1 = s1.endpoints[0].coordinates[0], s1.endpoints[0].coordinates[1]
    x2,y2 = s1.endpoints[1].coordinates[0], s1.endpoints[1].coordinates[1]
    x3,y3 = s2.endpoints[0].coordinates[0], s2.endpoints[0].coordinates[1]
    x4,y4 = s2.endpoints[1].coordinates[0], s2.endpoints[1].coordinates[1]
    denom = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)
    if denom == 0: # parallel
        return False,None,None
    ua = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / denom
    if ua < 0 or ua > 1: # out of range
        return False,None,None
    ub = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / denom
    if ub < 0 or ub > 1: # out of range
        return False,None,None
    x = x1 + ua * (x2-x1)
    y = y1 + ua * (y2-y1)
    return True, x,y

def point_dans_poly(p,pol):
    """
    test si un point p est dans un polygone pol en cherchant 
    l'intersection du segment vertical de p jusqu'au bout 
    de la feuille et un segment du polygone.
    """
    # print('=============================================================')
    # print(p)
    # print('=============================================================')
    s=Segment([p,Point([p.coordinates[0], Polygon.ABS_MIN_Y - 1])])
    compt=0
    mem_pour_dist=None
    erreur_arrondi = 0.000001

    
    # take the last point as a reference for the first segment, if last segment is horizontal take the one before
    curr_x = pol.points[0].coordinates[0]
    for i in range(-1, -len(pol.points), -1):
        if curr_x == pol.points[i].coordinates[0]:  # is horizontal
            continue
        
        x_ancien = pol.points[i].coordinates[0]
        break

    for segment in pol.segments():
        # print(segment)
        # check if segment if vertical
        if segment.endpoints[0].coordinates[0] == segment.endpoints[1].coordinates[0]:
            continue

        b,x,y= intersect(s,segment)
        # print(b, x, y)

        if b:
            if not mem_pour_dist or mem_pour_dist.coordinates[1] < y:
                mem_pour_dist = Point([x,y])

            if (abs(x - segment.endpoints[0].coordinates[0])<erreur_arrondi and abs(y-segment.endpoints[0].coordinates[1]) < erreur_arrondi):
                if (x_ancien > x and x > segment.endpoints[1].coordinates[0]) or (x_ancien < x and x < segment.endpoints[1].coordinates[0]):
                    x_ancien=segment.endpoints[0].coordinates[0]
                    continue
                
            compt +=1
            # print(compt)

        x_ancien=segment.endpoints[0].coordinates[0]

    if compt % 2 ==0:
        return False,None
    return True , mem_pour_dist


def poly_dans_poly(pol1,pol2, use_minmax=True):
    """ 
    test sut pol1 est dans pol2 et renvoie True ou False 
    et la distance entre le premier sommet de pol1 et le polygone pol2 dans le cas de l'inclusion
    on test au prealable que l'inclusion est possible par une simple verification de dimensions
    """

    # Si les extrémités du petit polygone sont au delà des extrémités du grand, inclusion impossible
    if use_minmax:
        if pol1.min_x < pol2.min_x or \
        pol1.max_x > pol2.max_x or \
        pol1.min_y < pol2.min_y or \
        pol1.max_y > pol2.max_y:
            return False, None

    b,point_rencontre=point_dans_poly(pol1.points[0],pol2)
    if b:
        distance = pol1.points[0].distance_to(point_rencontre)
        return True,distance
    return False, None


def poly_dans_poly2(pol1,pol2, use_minmax=True):
    """ 
    test sut pol1 est dans pol2 et renvoie True ou False 
    et la distance entre le premier sommet de pol1 et le polygone pol2 dans le cas de l'inclusion
    on test au prealable que l'inclusion est possible par une simple verification de dimensions
    """

    # Si les extrémités du petit polygone sont au delà des extrémités du grand, inclusion impossible
    if use_minmax:
        if pol1.min_x < pol2.min_x or \
        pol1.max_x > pol2.max_x or \
        pol1.min_y < pol2.min_y or \
        pol1.max_y > pol2.max_y:
            return False

    for point in pol1.points[1:]:
        if point_dans_poly(pol1.points[0],pol2)[0] != point_dans_poly(point, pol2)[0]:
            print("fuck")
    return True