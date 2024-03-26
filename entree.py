#!/usr/bin/env python3

import random
import math
import tqdm
from geo.point import Point
from geo.segment import Segment
from geo.polygon import Polygon, couples
from algo2 import intersect


# Cas 1 : Génération de triangles


def genere_triangle():
    triangle = []
    for _ in range(3):
        x, y = random.randrange(1000), random.randrange(1000)
        triangle.append([x, y])
    return triangle


def intersection_triangle(triangle, liste_triangles):
    p1, p2, p3 = triangle
    p1 = Point([p1[0], p1[1]])
    p2 = Point([p2[0], p2[1]])
    p3 = Point([p3[0], p3[1]])
    s1_2 = Segment([p1, p2])
    s2_3 = Segment([p2, p3])
    s3_1 = Segment([p3, p1])
    for autre_triangle in liste_triangles:
        t1, t2, t3 = autre_triangle
        polygon = Polygon([Point(t1), Point(t2), Point(t3)])
        for segment in polygon.segments():
            if intersect(s1_2, segment) or intersect(s2_3, segment) or intersect(s3_1, segment):
                return True
    return False


# Cas 2 : Génération de polygones quelconques


def do_segment_intersect(all_segments, target_segment):
    for segment in all_segments:
        if intersect(segment, target_segment)[0]:
            return True
    return False

def genere_polygone(deltas):
    window_max = 10000
    window_min = -10000
    num_tries = 600
    n = random.randint(2, 20) # nb de cotés du polygone
    p1 = Point([random.randint(window_min, window_max), random.randrange(window_min, window_max)])
    
    points = [p1]
    last_point = p1
    for segment_num in range(n):
        for try_num in range(num_tries):
            sign_x = random.choice([-1, 1])
            sign_y = random.choice([-1, 1])

            delta_x = random.randint(1, deltas) * sign_x
            delta_y = random.randint(1, deltas) * sign_y

            p = Point([last_point.coordinates[0] + delta_x, last_point.coordinates[1] + delta_y])
            if p.coordinates[0] > window_max or p.coordinates[0] < window_min or p.coordinates[1] > window_max or p.coordinates[1] < window_min:
                continue
            
            points.append(p)

            all_segments = list(map(Segment, couples(points)))

            if do_segment_intersect(all_segments[:-3], all_segments[-2]):  # how is this working
                points.pop()
                continue

            # verify that new segment is not on the previous one, by checking the last point on
            # the new segment
            if len(points) > 2 and Segment([points[-3], points[-2]]).contains(points[-1]):
                points.pop()
                continue
            
            elif segment_num == n-1 and do_segment_intersect(all_segments[1:-2], all_segments[-1]):
                points.pop()
                continue

            break
        if try_num == num_tries-1:
            return False
        last_point = points[-1]
    return Polygon(points)


def intersection_poly(poly, liste_poly):
    for autre_poly in liste_poly:
        for segment in poly.segments():
            for autre_segment in autre_poly.segments():
                if intersect(segment, autre_segment)[0]:
                    return True
    return False


def genere_entree_poly(N):
    liste_poly = []
    deltas = 1000
    for i in tqdm.tqdm(range(N)):
        poly = genere_polygone(max(math.floor(deltas), 5))
        while not poly or intersection_poly(poly, liste_poly):
            poly = genere_polygone(max(math.floor(deltas), 5))
            deltas *= 0.999
        deltas += 20
        liste_poly.append(poly)
        for point in poly.points:
            print(f"{i} {point.coordinates[0]} {point.coordinates[1]}")


def genere_entree_triangle(N):
    liste_triangles = []
    for i in range(N):
        triangle = genere_triangle()
        while intersection_triangle(triangle, liste_triangles):
            triangle = genere_triangle()
        liste_triangles.append(triangle)
        for point in triangle:
            print(f"{i} {point[0]} {point[1]}")


N= random.randint(1, 1000)
genere_entree_poly(N)