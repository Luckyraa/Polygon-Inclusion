import os
import time
import traceback
from typing import Tuple, Callable, Optional
from colorama import Fore
import subprocess as sp

CheckFunction = Callable[[str, str], bool]
PYTHON_COMMAND = os.getenv("POLY_PYTHON", "python3")
print(f"Python command: {PYTHON_COMMAND}")

def timed_exec(program, argument, timeout) -> Tuple[str, float]:
    """Runs the main program on the given input and measures how much time it took."""
    t0 = time.perf_counter()
    process = sp.run([PYTHON_COMMAND, program, argument], timeout=timeout, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)
    t1 = time.perf_counter()
    elapsed = t1-t0

    process.check_returncode()

    output = str(process.stdout).strip()
    warnings = str(process.stderr).strip()
    if warnings:
        print("...")
        print(f"{Fore.YELLOW}========== PROGRAM WARNINGS ON STDERR ==========")
        print(warnings)

    return output, elapsed


def tested_exec(bench, poly_name, poly_path, check: CheckFunction) -> Optional[float]:
    """
    Runs the main program and checks that the output is correct,
    according to the given checking function.
    :param check: a function that returns True iff the result is correct
    """
    failed = bench.failed
    passed = bench.passed
    try:
        output, elapsed = timed_exec(bench.user_program, poly_path, bench.program_timeout)
    except sp.TimeoutExpired:
        failed(poly_name, 60, "timeout")
    except sp.CalledProcessError as ex:
        failed(poly_name, None, f"run crashed with exit code {ex.returncode}")
        print(ex.stderr)
        print(ex.stdout)
    except:
        failed(poly_name, None, "run crashed")
        traceback.print_exc()
    else:
        if output is None:
            failed(poly_name, elapsed, "returned None")
        else:
            try:
                check = check(output, poly_path)
            except:
                failed(poly_name, elapsed, "checks crashed")
                traceback.print_exc()
            else:
                if not check:
                    failed(poly_name, elapsed, "wrong result")
                    print(f"wrong result is: {output}")
                else:
                    passed(poly_name, elapsed)
                    return elapsed
    return None


def run_generator(file, options, env, timeout):
    """Generates a test file if it doesn't exist yet. Calls generator.py with the given options."""
    if not os.path.exists(file):
        print(f"Generating '{file}'... ", end="")
        try:
            with open(file, "w") as output:
                gen_command = [PYTHON_COMMAND, "generate.py"] + options.split(" ")
                gen_process = sp.run(gen_command, timeout=timeout, stdout=output, stderr=sp.PIPE, env=env, universal_newlines=True)
                gen_process.check_returncode()
        except BaseException as ex:
            print(f"{Fore.RED}FAILED")
            if os.path.exists(file):
                os.remove(file) # cleanup to avoid corrupted .poly files
            raise Exception("Polygon generation failed") from ex
        else:
            messages = str(gen_process.stderr).strip()
            if "PARENT" in messages:
                answer_file = file.replace(".poly", ".answer")
                try:
                    answer_list = []
                    for msg in messages.split("\n"):
                        if msg.startswith("PARENT"):
                            parts = msg.split(" ")
                            parent_id = int(parts[2])
                            answer_list.append(parent_id)
                        else:
                            print(f"{Fore.YELLOW}{msg}")
                    with open(answer_file, "w") as answer:
                        answer.write(str(answer_list))
                except BaseException as ex:
                    print(f"{Fore.RED}FAILED")
                    os.remove(file)
                    if os.path.exists(answer_file):
                        os.remove(answer_file)
                    raise Exception("Polygon generation failed (in messages processing)") from ex

            print(f"{Fore.GREEN}Done")
