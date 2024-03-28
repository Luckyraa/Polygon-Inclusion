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


def trouve_inclusions(polygones):
    """
    renvoie le vecteur des inclusions
    la ieme case contient l'indice du polygone
    contenant le ieme polygone (-1 si aucun).
    (voir le sujet pour plus d'info)
    """
    num_lignes = floor(sqrt(len(polygones)/10))
    zones.separate_polygons_to_zones(polygones, num_lignes, num_lignes)
    
    table=[-1 for _ in range(len(polygones))]
    i=0
    for p in polygones:
        j=0
        min_dist=None
        poly_proche=None
        for g in p.zone:
            if g!=p:
                b,dist=poly_dans_poly(p,g, True)
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
        """
        mesure le temps d'execution du programme
        """
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
        inclusions = trouve_inclusions(polygones)
        print(inclusions)


if __name__ == "__main__":
    main()
