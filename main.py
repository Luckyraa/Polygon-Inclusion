#!/usr/bin/env python3
"""
fichier principal pour la detection des inclusions.
ce fichier est utilise pour les tests automatiques.
attention donc lors des modifications.
"""
from math import pi, sqrt, floor
from geo.point import Point
from geo.segment import Segment
import sys
from tycat import read_instance
from algo2 import poly_dans_poly
import zones
import datetime



def trouve_presque_inclusions(polygones):
    """
    renvoie le vecteur des inclusions
    la ieme case contient l'indice du polygone
    contenant le ieme polygone (-1 si aucun).
    (voir le sujet pour plus d'info)
    """
    table=[-1 for _ in range(len(polygones))]
    i=0
    for p in polygones:
        j=0
        min_dist=None
        poly_proche=None
        for g in polygones:
            if g!=p:
                b,dist=poly_dans_poly(p,g)
                if b:
                    if min_dist is None:
                        poly_proche=j
                        min_dist=dist
                    else:
                        if dist<min_dist:
                            poly_proche=j
                            min_dist=dist
            j+=1
        if poly_proche is not None:
            table[i]=poly_proche
        i+=1
    return table


def trouve_inclusions(polygones):
    """
    renvoie le vecteur des inclusions
    la ieme case contient l'indice du polygone
    contenant le ieme polygone (-1 si aucun).
    (voir le sujet pour plus d'info)
    """
    table=[-1 for _ in range(len(polygones))]
    i=0
    for p in polygones:
        j=0
        min_dist=None
        poly_proche=None
        for g in p.zone:
            if g!=p:
                # v1 = poly_dans_poly(p,g, True)
                # v2 = poly_dans_poly(p,g, False)
                # if v1 != v2:
                #     print("fuck")  # there are still fucks, check why
                #     poly_dans_poly(p,g, False)

                b,dist=poly_dans_poly(p,g)
                if b:
                    if min_dist is None:
                        poly_proche=polygones.index(g)
                        min_dist=dist
                    else:
                        if dist<min_dist:
                            poly_proche=polygones.index(g)
                            min_dist=dist
            j+=1
        if poly_proche is not None:
            table[i]=poly_proche
        i+=1
    return table



def tests(polygones):

        start = datetime.datetime.now()
        inclusions = trouve_presque_inclusions(polygones)
        print('naif')
        print(datetime.datetime.now() - start)
        print(inclusions)

        start = datetime.datetime.now()
        zones.separate_polygons_to_zones(polygones, 1, 0)
        inclusions = trouve_inclusions(polygones)
        print('with 2 zone')
        print(datetime.datetime.now() - start)
        print(inclusions)

        start = datetime.datetime.now()
        zones.separate_polygons_to_zones(polygones, 1, 1)
        inclusions = trouve_inclusions(polygones)
        print('with 4 zone')
        print(datetime.datetime.now() - start)
        print(inclusions)

        start = datetime.datetime.now()
        zones.separate_polygons_to_zones(polygones, 2, 2)
        inclusions = trouve_inclusions(polygones)
        print('with 9 zone')
        print(datetime.datetime.now() - start)
        print(inclusions)

        start = datetime.datetime.now()
        zones.separate_polygons_to_zones(polygones, 3, 3)
        inclusions = trouve_inclusions(polygones)
        print('with 16 zone')
        print(datetime.datetime.now() - start)
        print(inclusions)

        start = datetime.datetime.now()
        zones.separate_polygons_to_zones(polygones, 7, 7)
        inclusions = trouve_inclusions(polygones)
        print('with 64 zone')
        print(datetime.datetime.now() - start)
        print(inclusions)

        start = datetime.datetime.now()
        zones.separate_polygons_to_zones(polygones, 19, 19)
        inclusions = trouve_inclusions(polygones)
        print('with 400 zone')
        print(datetime.datetime.now() - start)
        print(inclusions)

        start = datetime.datetime.now()
        zones.separate_polygons_to_zones(polygones, 29, 29)
        inclusions = trouve_inclusions(polygones)
        print('with 900 zone')
        print(datetime.datetime.now() - start)
        print(inclusions)

        # ideal number of zones
        start = datetime.datetime.now()
        num_lignes = floor(sqrt(len(polygones)))
        zones.separate_polygons_to_zones(polygones, num_lignes, num_lignes)
        inclusions = trouve_inclusions(polygones)
        print(f'with {num_lignes**2} zone')
        print(datetime.datetime.now() - start)
        print(inclusions)


def main():
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """
    for fichier in sys.argv[1:]:
        polygones = read_instance(fichier)
        num_lignes = floor(sqrt(len(polygones)))
        zones.separate_polygons_to_zones(polygones, num_lignes, num_lignes)
        inclusions = trouve_inclusions(polygones)
        print(inclusions)


if __name__ == "__main__":
    main()
