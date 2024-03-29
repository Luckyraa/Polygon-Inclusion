"""
Functions that check the result of the user program.
"""
import ast
from typing import Optional

from colorama import Fore


def check_eq(expected: str):
    def check(res, _):
        return res == expected
    return check


def check_nested(n: int):
    def check(res, _):
        array = ast.literal_eval(res)
        if len(array) != n:
            return False
        for k in range(n):
            if array[k] != k - 1:
                return False
        return True

    return check


def check_nested_then_independent(k0: int, n_nested: int, n_total: int):
    def check(res, _):
        array = ast.literal_eval(res)
        if len(array) != n_total:
            return False
        for k in range(n_total):
            if k < n_nested and array[k] != k + k0:
                return False
            elif k >= n_nested and array[k] != -1:
                return False
        return True

    return check


def check_all_in_last(n: Optional[int]):
    def check(res, _):
        array = ast.literal_eval(res)
        l = len(array) if n is None else n
        assert l > 0
        return len(array) == l and array[l - 1] == -1 and all(e == l - 1 for e in array[:-1])

    return check


def check_independent(n: int):
    def check(res, _):
        array = ast.literal_eval(res)
        actual_n = len(array)
        if actual_n != n:
            print(f"{Fore.RED}Wrong result size, expected {n} but got {actual_n}")
            return False
        wrong = next(filter(lambda e: e[1] != -1, enumerate(array)), None)
        if wrong is not None:
            print(f"{Fore.RED}Wrong result: {wrong[1]} at position {wrong[0]}, expected -1")
            return False
        return True

    return check


def check_file():
    def check(res, poly_file):
        answer_file = poly_file.replace(".poly", ".answer")
        with open(answer_file, "r") as f:
            expected = f.readline().strip()
        actual = res.strip()
        if actual != expected:
            actual_array = ast.literal_eval(actual)
            expected_array = ast.literal_eval(expected)
            wrong = next(filter(lambda e: e[1] != expected_array[e[0]], enumerate(actual_array)))
            print("expected result:", expected)
            print(f"{Fore.RED}Wrong result: {wrong[1]} at position {wrong[0]}, expected {expected_array[wrong[0]]}")
        return actual == expected

    return check

def check_nothing():
    def no_check(a,b):
        print(f"{Fore.CYAN}The result is not checked for this test.")
        return True

    return no_check