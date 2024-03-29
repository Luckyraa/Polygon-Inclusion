#!/usr/bin/env python3
# coding: utf-8

# Génère des jeux de test.
import sys

from pat.gen import result_polygon, DEOPT_FACTOR
from pat.gen.circles import nested_circles, aligned_circles
from pat.gen.hexagons import recursive_hexagons
from pat.gen.puzzle import puzzle
from pat.gen.sierpinski import almost_sierpinski
from pat.gen.squares import nested_squares, aligned_squares, fake_nested_squares
from pat.gen.squarefractals import square_fractals
from pat.gen.territory import run_agent_battle
from pat.geo.vector import Vector

option_index = 0
def get(options, f, default=None):
    global option_index
    try:
        value = options[option_index]
        option_index += 1
        return f(value)
    except IndexError:
        if default is None:
            exit("Missing parameter")
        else:
            return default

def generate_sierpinski(options):
    depth = get(options, int)
    base = result_polygon([Vector(0, 0), Vector(300, 0), Vector(150, 259.998)])
    yield from almost_sierpinski(base, 2.0, 0.5, depth)
    yield base


def generate_nested_squares(options):
    depth = get(options, int)
    spacing = get(options, float, 1.0)
    x0, y0, s0 = 0, 0, depth/spacing
    return nested_squares(x0, y0, s0, spacing, depth)


def generate_aligned_squares(options):
    n = get(options, int)
    side = get(options, float, 10)
    shift_x = get(options, float, side+1)
    shift_y = get(options, float, 0)
    return aligned_squares(0, 0, side, shift_x, shift_y, n)


def generate_square_grid(options):
    lines = get(options, int)
    columns = get(options, int, lines)
    side = get(options, float, 10)
    shift = get(options, float, side+1)
    for k in range(lines):
        yield from aligned_squares(0, shift*k, side, shift, 0, columns)

def generate_square_fractal(options):
    depth = get(options, int)
    return square_fractals(depth)

def generate_nested_circles(options):
    depth = get(options, int)
    n_points = get(options, int, 360)
    spacing = get(options, float, 1.0)
    return nested_circles(300, 300, depth/spacing, spacing, n_points, depth)


def generate_aligned_circles(options):
    n = get(options, int)
    n_points = get(options, int, 360)
    radius = get(options, float, 10)
    shift_x = get(options, float, 2*radius+1)
    shift_y = get(options, float, 0)
    return aligned_circles(0,0, radius, shift_x, shift_y, n_points, n)


def generate_circle_grid(options):
    lines = get(options, int)
    columns = get(options, int, lines)
    n_points = get(options, int, 360)
    radius = get(options, float, 10)
    shift = get(options, float, 2*radius+1)
    for k in range(lines):
        yield from aligned_circles(0, shift * k, radius, shift, 0, n_points, columns)


def generate_hexagons(options):
    depth = get(options, int)
    center = Vector(0, 0)
    side = get(options, float, 3000)
    return recursive_hexagons(depth, center, side)

def generate_puzzle(options):
    width = get(options, int)
    height = get(options, int, width)
    spacing = get(options, float, 1.05)
    return puzzle(width, height, spacing)


def generate_territory(options):
    width = get(options, int)
    height = get(options, int, width)
    agents = get(options, int, 10)
    turns = get(options, int, 50)
    seed = get(options, int, 424242)
    return run_agent_battle(width, height, agents, 0, turns, seed)

def generate_fakesqnest(options):
    num = get(options, int)
    polygons = fake_nested_squares(0, 0, num)
    return list(polygons)

def not_found(options):
    print(f"No such generator: {sys.argv[1]}")
    print("Available names:", list(GENERATORS.keys()))
    exit(1)


GENERATORS = {
    "sierp": generate_sierpinski,
    "sqnest": generate_nested_squares,
    "sqline": generate_aligned_squares,
    "sqgrid": generate_square_grid,
    "sqfrac": generate_square_fractal,
    "circnest": generate_nested_circles,
    "circline": generate_aligned_circles,
    "circgrid": generate_circle_grid,
    "fakesqnest": generate_fakesqnest,
    "hexa": generate_hexagons,
    "puzzle": generate_puzzle,
    "battle": generate_territory
}


def main():
    if len(sys.argv) == 1:
        print("Missing argument: generator name")
        print("Available names:", list(GENERATORS.keys()))
        exit(1)

    assert DEOPT_FACTOR >= 1, "Wrong DEOPT_FACTOR, must be >= 1"

    generator = sys.argv[1]
    options = sys.argv[2:]
    polygons = GENERATORS.get(generator, not_found)(options)
    n_polys, n_points = 0, 0
    for i,poly in enumerate(polygons):
        if poly.parent is not None:
            print("PARENT", i, poly.parent, file=sys.stderr)
        for point in poly.points:
            print(i, point.x, point.y)
            n_points += 1
        n_polys += 1
    print(n_polys, "polys,", n_points, "pts", end=" ", file=sys.stderr)


if __name__ == '__main__':
    main()
