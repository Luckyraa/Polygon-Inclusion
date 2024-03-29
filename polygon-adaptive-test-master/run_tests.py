#!/usr/bin/env python3
# coding: utf-8

"""
Lance les tests, vérifie le résultat et mesure la performance.
NÉCESSITE PYTHON >= 3.6
- 3.5+ pour la fonction subprocess.run
- 3.6+ pour les f-strings
"""
import os
import sys
import time
from typing import Callable

from colorama import init as colorama_init

from pat.test.bench import TestBench
from pat.test.checking import *


# ---- Meta-tests ----
def available_tests():
    for name in globals():
        if name.startswith("test_"):
            var = globals()[name]
            if isinstance(var, Callable):
                yield name, var

def test_all(bench):
    for name, func in available_tests():
        if name not in ("test_all", "test_adaptative"):
            func(bench)

def test_adaptative(bench):
    for name, func in available_tests():
        if name not in ("test_all", "test_fast", "test_adaptative"):
            func(bench)

# ---- Tests definitions ----
def test_fast(bench: TestBench):
    bench.add_handmade_family("fast")\
         .add_test("10x10",  check_eq("[-1, 0]"))\
         .add_test("e2", check_eq("[1, -1, 0, 0]"))\
         .add_test("no-inclusion-1", check_independent(5))\
         .add_test("no-inclusion-2", check_independent(7))\
         .add_test("inclusions-nested", check_nested(11))\
         .add_test("inclusions-1", check_eq("[-1, 0, 6, -1, 5, -1, -1]"))\
         .add_test("edge-case-intersect-on-vertex-1", check_eq("[1, 2, -1]"))\
         .add_test("edge-case-intersect-on-vertex-2", check_eq("[1, 2, 3, -1]"))\
         .add_test("edge-case-intersect-on-vertex-3", check_eq("[1, 2, 3, 4, -1]"))\
         .add_test("edge-case-ray-on-side", check_nested_then_independent(1, 2, 45))\
         .add_test("yet-another-test", check_eq("[3, 25, 25, 25, 25, 25, 25, 6, 6, 10, 25, 25, 4, 5, 11, 0, 25, 21, 21, 21, 25, 25, 25, 25, 25, -1, 25]"))\
         .add_test("points-points-points", check_eq("[-1, -1, -1, -1, -1, 4, 2, 2, 2]")) \
         .add_test("broken-puzzle", check_independent(4))

def test_sierp(bench: TestBench):
    def sierpinski_n(param):
        """Nombre de polygones dans un test 'sierpinski' de paramètre param"""
        return (3**param + 1)//2  # u(n+1) = u(n) + 3**n et u(0) = 0

    bench.add_family("sierpinski", "sierp {}", lambda p: check_all_in_last(sierpinski_n(p)))\
         .add_serie(param0=4, increment=1, max_times=11)

def test_sqnest(bench):
    bench.add_family("sqnest", "sqnest {}", lambda p: check_nested(p)) \
         .add_serie(500, 500, 8) \
         .add_serie(10_000, 10_000, 5)

def test_sqline(bench):
    bench.add_family("sqline", "sqline {}", lambda p: check_independent(p)) \
         .add_serie(500, 500, 8) \
         .add_serie(10_000, 10_000, 5)

def test_sqgrid(bench):
    bench.add_family("sqgrid", "sqgrid {0} {0}", lambda p: check_independent(p*p)) \
         .add_serie(40, 10, 8) \
         .add_serie(300, 100, 8)

def test_sqfrac(bench):
    checks = {
        2: check_eq("[4, 4, 4, 4, -1]"),
        3: check_eq("[20, 20, 20, 20, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, -1]"),
    }
    bench.add_family("sqfrac", "sqfrac {0}", lambda p: checks.get(p, check_nothing())) \
         .add_serie(2, 1, 8)

def test_circnest(bench):
    bench.add_family("circnest", "circnest {} 360", lambda p: check_nested(p)) \
         .add_serie(10, 10, 8) \
         .add_serie(500, 500, 6) \
         .add_serie(5000, 5000, 4)

def test_circline(bench):
    bench.add_family("circline", "circline {} 360", lambda p: check_independent(p)) \
        .add_serie(10, 10, 8) \
        .add_serie(500, 500, 8)

def test_circgrid(bench):
    # 36 points per circle
    bench.add_family("circgrid-36", "circgrid {0} {0} 36", lambda p: check_independent(p * p)) \
         .add_serie(40, 10, 8) \
         .add_serie(300, 100, 8)

    # 360 points!
    bench.add_family("circgrid-360", "circgrid {0} {0} 360", lambda p: check_independent(p * p)) \
         .add_serie(40, 10, 8) \
         .add_serie(300, 100, 8)

def test_hexa(bench):
    def hexa_n(param):
        """Nombre de polygones dans un test 'hexa' de paramètre param."""
        return (6**param - 1)//5 # u(n+1) = u(n) + 6**n; u(1) = 1

    bench.add_family("hexagons", "hexa {}", lambda p: check_independent(hexa_n(p))) \
         .add_serie(2, 1, 8)

def test_fakesqnest(bench):
    bench.add_family("fakesqnest", "fakesqnest {}", lambda p: check_independent(p)) \
        .add_serie(40, 10, 8) \
        .add_serie(300, 100, 8)
        
def test_puzzle(bench):
    bench.add_family("puzzle", "puzzle {0} {0}", lambda p: check_independent(4*p*p))\
         .add_serie(50, 25, 7) \
         .add_serie(300, 100, 3)

def test_battle(bench):
    bench.add_family("battle-100x100", "battle 100 100 {0} 250 424242", lambda p: check_file()) \
         .add_serie(50, 50, 4) \
         .add_serie(500, 250, 8)
    # Il y a encore des cas où la "solution" est fausse.
    # Il faudrait utiliser un algo complet pour l'obtenir, mais je ne peux pas l'ajouter au framework :)
    bench.add_family("battle-1000x1000", "battle 1000 1000 {0} 200 2020", lambda p: check_nothing()) \
         .add_serie(1000, 1000, 8)

# ---- Arguments ----
def get_user_program():
    user_program = "/home/sacha/Algo/algo_capiomot_ederys/main.py"
    if not user_program:
        # Essaie de trouver le projet d'algo dans un dossier frère
        for dir in os.listdir(".."):
            if dir.startswith("algo_"):
                readme = f"../{dir}/README.md"
                main_py = f"../{dir}/main.py"
                if os.path.isfile(readme) and os.path.isfile(main_py):
                    print(f"{Fore.YELLOW}No environment variable POLY_PROGRAM, but found {main_py}")
                    user_program = main_py
                    break
        if not user_program:
            print("Program main.py not found, please specify POLY_PROGRAM like this:")
            print("\texport POLY_PROGRAM=\"path/to/algo_project/main.py\"")
            exit(1)

    return os.path.abspath(user_program)

def get_user_timeout():
    return int(os.getenv("POLY_TIMEOUT", "60"))

def get_gen_timeout():
    return int(os.getenv("POLY_GEN_TIMEOUT", "240"))

def get_output_dir(user_program):
    dir = "/home/sacha/Algo/algo_capiomot_ederys/resultats"
    if not dir:
        dir = os.path.join(os.path.dirname(user_program), "tests")
        print(f"{Fore.YELLOW}No environment variable POLY_OUTPUT specified, using {dir}")
    return dir

def get_n_repetitions():
    if len(sys.argv) < 2:
        print("Missing argument: number of global repetitions (int)")
        print("Run with --help to get help")
        exit(2)
    return int(sys.argv[1])

def get_deopt_factors():
    fact = os.getenv("DEOPT_FACTOR")
    if fact is None:
        print(f"{Fore.CYAN}Suggestion: export DEOPT_FACTOR=1,5")
        print(f"{Fore.YELLOW}No environment variable DEOPT_FACTOR specified, using \"1\". Try it :-D")
    return map(int, os.getenv("DEOPT_FACTOR", "1").split(","))

def get_tests():
    args = sys.argv[2:]
    if len(args) == 0:
        print("Missing arguments: names of the tests to execute")
        print("Run with --list for a list of available tests")
        exit(2)

    for test_name in args:
        test_function = globals().get(f"test_{test_name}")
        if test_function is None:
            print(f"{Fore.RED}Unknown test '{test_name}'.")
            exit(1)

        yield test_function

# ---- Main program ----
def main():
    colorama_init(autoreset=True) # initializes the color system

    if sys.version_info < (3, 6):
        print(f"{Fore.RED}This script requires PYTHON >= 3.6")
        exit(1)

    if len(sys.argv) == 2:
        if sys.argv[1] == "--help":
            print("Usage: ./run_tests.py REP TEST...")
            print("Runs tests on your algo project, checks results and measures performance.")
            print("\nArguments:")
            print("  REP\t\t\tnumber of repetitions")
            print("  TEST\t\t\tthe test(s) to run, separated by spaces")
            print("\nEnvironment variables:")
            print("  POLY_PROGRAM\t\tpath to your main.py file")
            print("  POLY_TIMEOUT\t\ttimeout (in seconds) for your program")
            print("  POLY_GEN_TIMEOUT\ttimeout for the polygon generator")
            print("  POLY_OUTPUT\t\tdirectory where to put the results")
            print("\nContribute at https://gitlab.ensimag.fr/raffingu/polygon-adaptive-test ^_^")
        elif sys.argv[1] == "--list":
            print("Possible values for argument(s) TEST:")
            print(", ".join((name.replace("test_", "") for name,f in available_tests())))
        else:
            print("Invalid option. Run with --help for help")
            exit(1)
        exit(0)

    # Parse arguments and environment variables
    user_program = get_user_program()
    user_timeout = get_user_timeout()
    generator_timeout = get_gen_timeout()
    output_directory = get_output_dir(user_program)
    repetitions = get_n_repetitions()
    deopt_factors = get_deopt_factors()
    tests = get_tests()

    # Run the tests
    bench = TestBench(user_program, user_timeout, generator_timeout, output_directory)
    for function in tests:
        function(bench)
    bench.prepare()

    t0 = time.perf_counter()
    for deopt in deopt_factors:
        bench.run(user_program, repetitions, deopt)
    total_elapsed = time.perf_counter() - t0

    print("-" * 50)
    print(f"Results saved in {bench.reports_dir}/")
    print(f"Benchmark completed in {total_elapsed} seconds.")
    total = bench.n_passed + bench.n_failed
    if total == bench.n_passed:
        print(f"{Fore.GREEN}{bench.n_passed}/{total} tests passed.")
    elif total == bench.n_failed:
        print(f"{Fore.RED}{bench.n_failed}/{total} tests failed!")
    else:
        print(f"{Fore.YELLOW}{bench.n_passed}/{total} tests passed.")


if __name__ == '__main__':
    main()
