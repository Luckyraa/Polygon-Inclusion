#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
exemple d'utilisation du module geo
"""
from geo.point import Point
from geo.tycat import tycat
from geo.segment import Segment
from geo.polygon import Polygon
import sys
from tycat import read_instance


def intersect(s1, s2):
    s1_x1,s1_y1 = s1.endpoints[0].coordinates[0], s1.endpoints[0].coordinates[1]
    s1_x2,s1_y2 = s1.endpoints[1].coordinates[0], s1.endpoints[1].coordinates[1]
    s2_x1,s2_y1 = s2.endpoints[0].coordinates[0], s2.endpoints[0].coordinates[1]
    s2_x2,s2_y2 = s2.endpoints[1].coordinates[0], s2.endpoints[1].coordinates[1]
    denom = (s2_y2-s2_y1)*(s1_x2-s1_x1) - (s2_x2-s2_x1)*(s1_y2-s1_y1)
    if denom == 0: # parallel
        #if (s1.contains(s2.endpoints[0].coordinates) and s1.contains(s2.endpoints[1].coordinates)) or (s2.contains(s1.endpoints[0].coordinates) and s2.contains(s1.endpoints[1].coordinates)):
        #   return 1
        return False
    ua = ((s2_x2-s2_x1)*(s1_y1-s2_y1) - (s2_y2-s2_y1)*(s1_x1-s2_x1)) / denom
    if ua < 0 or ua > 1: # out of range
        return False
    ub = ((s1_x2-s1_x1)*(s1_y1-s2_y1) - (s1_y2-s1_y1)*(s1_x1-s2_x1)) / denom
    if ub < 0 or ub > 1: # out of range
        return False
    #x = x1 + ua * (x2-x1)
    #y = y1 + ua * (y2-y1)
    return True

def point_dans_poly(p,pol):
    s=Segment([p,Point([0.0,0.0])])
    compt=0
    for segment in pol.segments():
        if intersect(s,segment):
            compt +=1
    if compt % 2 !=0:
        return False
    return True

def poly_dans_poly(pol1,pol2):
    #pol1 dans pol2
    for p in pol1.points:
        if not(point_dans_poly(p,pol2)):
            return False
    return True
        
def trouve_inclusions(polygones):
    table=[[False for _ in range(4)] for _ in range(4)]
    i=0
    for p in polygones:
        j=0
        for g in polygones:
            print(p,g,poly_dans_poly(p,g))
            table[i][j]=poly_dans_poly(p,g)
            j+=1
        i+=1
    return table


def main():
    for fichier in sys.argv[1:]:
        polygones = read_instance(fichier)
        inclusions = trouve_inclusions(polygones)
        print(inclusions)

main()
