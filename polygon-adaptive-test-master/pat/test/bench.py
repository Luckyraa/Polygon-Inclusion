import time
import os
import traceback
from datetime import datetime
from typing import Callable
from colorama import Fore
from .exec import run_generator, tested_exec, CheckFunction

CheckFunctionSupplier = Callable[[int], CheckFunction]

def create_report(directory, program_path, repetitions):
    now = datetime.today().strftime("%Y-%m-%d_%H:%M")
    program_name = program_path.rsplit("/", 1)[-1]
    report_file = f"{directory}/{now} (x{repetitions}) {program_name}.csv"
    f = open(report_file, "w")
    f.write("name;ok;time\n")
    return f


class TestSerie:
    def __init__(self, param0: int, increment: int, max_times: int):
        self.param0 = param0
        self.increment = increment
        self.max_times = max_times

    def run(self, family, bench, deopt):
        deopt_suffix = "-deopt{}".format(deopt) if deopt > 1 else ""
        env = {"DEOPT_FACTOR": str(deopt)}
        runs, elapsed = 0, 0
        param = self.param0
        while runs < self.max_times and elapsed is not None:
            gen_options = family.generation.format(param)
            poly_name = gen_options.replace(" ", '-') + deopt_suffix
            poly_file = bench.poly_file(poly_name)
            try:
                run_generator(poly_file, gen_options, env, bench.generator_timeout)
            except:
                traceback.print_exc()
                print(f"{Fore.RED}Looks like the polygon generator crashed :'( Not enough RAM ?")
                break  # stop this serie
            else:
                elapsed = tested_exec(bench, poly_name, poly_file, family.check(param))
                if elapsed is None:  # the test failed
                    break
                else:
                    param += self.increment
                    runs += 1

        return runs


class TestFamily:
    def __init__(self, name, generation: str, check: CheckFunctionSupplier):
        self.name = name
        self.generation = generation
        self.check = check
        self.series = []

    def add_serie(self, param0: int, increment: int, max_times: int):
        self.series.append(TestSerie(param0, increment, max_times))
        return self

    def run(self, bench, deopt):
        ok, total = 0, sum(s.max_times for s in self.series)
        for s in self.series:
            n_ok = s.run(self, bench, deopt)
            ok += n_ok
            if n_ok < s.max_times:
                break
        print(f"{Fore.YELLOW}Completed {ok}/{total} adaptative tests in family '{self.name}'.")

class HandmadeTestFamily:
    def __init__(self, name):
        self.name = name
        self.tests = []

    def add_test(self, poly_name: str, check: CheckFunction):
        here = os.path.realpath(__file__)  # path to this file bench.py
        poly_file = os.path.join(here, f"../../../handmade-tests/{self.name}", f"{poly_name}.poly")
        poly_file = os.path.abspath(poly_file)
        if not os.path.isfile(poly_file):
            raise FileNotFoundError(poly_file)
        self.tests.append((poly_name, poly_file, check))
        return self

    def run(self, bench, deopt):
        ok, total = 0, len(self.tests)
        for t in self.tests:
            elapsed = tested_exec(bench, *t)
            if elapsed is not None:
                ok += 1
        print(f"{Fore.YELLOW}Completed {ok}/{total} handmade tests in family '{self.name}'.")

class TestBench:
    def __init__(self, user_program, program_timeout, generator_timeout, output_dir):
        self.user_program = user_program
        self.program_timeout = program_timeout
        self.generator_timeout = generator_timeout
        self.polygons_dir = output_dir + "/polygons"
        self.reports_dir = output_dir + "/reports"
        self.deopt_factor = 1
        self.n_failed = 0
        self.n_passed = 0
        self.families = []
        self.current_report = None

    def add_family(self, name: str, generation: str, check: CheckFunctionSupplier):
        family = TestFamily(name, generation, check)
        self.families.append(family)
        return family

    def add_handmade_family(self, name: str):
        family = HandmadeTestFamily(name)
        self.families.append(family)
        return family

    def prepare(self):
        os.makedirs(self.polygons_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)

    def run(self, program_path: str, repetitions=1, deoptimize_factor=1):
        with create_report(self.reports_dir, program_path, repetitions) as report:
            self.current_report = report
            t0 = time.perf_counter()
            for _ in range(repetitions):
                for f in self.families:
                    f.run(self, deoptimize_factor)
            t1 = time.perf_counter()
            return t1-t0

    def poly_file(self, poly_name):
        return f"{self.polygons_dir}/{poly_name}.poly"

    def passed(self, poly_file, elapsed):
        """Reports a passed (successfull) test"""
        print(f"{Fore.GREEN}PASSED {poly_file} in {elapsed} seconds")
        self.current_report.write(f"{poly_file};1;{elapsed}\n")
        self.current_report.flush()  # in case of a future crash, at least get the partial results
        self.n_passed += 1

    def failed(self, poly_file, elapsed, reason):
        """Reports a failed test"""
        print(f"{Fore.RED}FAILED {poly_file} in {elapsed} seconds ({reason})")
        self.current_report.write(f"{poly_file};0;{elapsed}\n")
        self.current_report.flush()
        self.n_failed += 1
