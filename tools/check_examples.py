"""Compile/run every standalone example in isolated temporary directories.

Usage: python tools/check_examples.py [--language all|python|c|java] [--sanitize]
Requires GCC-compatible cc and a JDK for their respective language checks.
No dependencies beyond the Python standard library; no repository build output.
"""

import argparse
from collections import Counter
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = (
    "Sorting-Algorithms", "Searching Algorithms", "Arrays", "Strings",
    "LinkedList", "Stack", "Queue", "Trees", "Heaps", "Graphs", "Greedy",
    "DynamicProgramming", "Backtracking", "BranchAndBound", "DivideAndConquer",
)
LANGUAGES = {"python": ".py", "c": ".c", "java": ".java"}


def run(command, stdin="", timeout=30):
    result = subprocess.run(command, input=stdin, text=True, encoding="utf-8",
                            capture_output=True, cwd=ROOT, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"Command failed ({result.returncode}): {command}\n"
                           f"{result.stdout}\n{result.stderr}")
    if result.stderr:
        raise RuntimeError(f"Unexpected diagnostics: {command}\n{result.stderr}")
    return result.stdout


def uses_menu(source):
    category = source.relative_to(ROOT).parts[0]
    if category == "Sorting-Algorithms":
        return not (source.suffix == ".c" and source.stem in ("BucketSort", "RadixSort"))
    if category == "Searching Algorithms":
        return source.suffix == ".py" or (source.suffix == ".java" and source.stem == "BinarySearch")
    return False


def input_case(source, values, key=None):
    tokens = [str(len(values)), *(str(value) for value in values)]
    if key is not None:
        tokens.append(str(key))
    if uses_menu(source):
        tokens = ["1", *tokens, "3"]
    return "\n".join(tokens) + "\n"


def check_sort(source, command):
    cases = [[], [7], [3, 1, 2], [7, 7, 7], [5, 4, 3, 2, 1], [0, 0, 0]]
    if source.stem != "RadixSort":
        cases.append([-5, 0, -2, -5])
    if source.stem == "CountingSort":
        cases += [[2147483647, 2147483646], [-2147483648, -2147483647]]
    else:
        cases.append([2147483647, 0, 42])
    if source.stem not in ("CountingSort", "RadixSort"):
        cases.append([-2147483648, 2147483647, 0])
    for values in cases:
        output = run(command, input_case(source, values))
        match = re.search(r"Sorted(?: Array)?:[ \t]*([^\r\n]*)", output)
        if match is None:
            raise AssertionError(f"No sorted output for {values}: {output}")
        actual = [int(item) for item in re.findall(r"-?\d+", match.group(1))]
        if actual != sorted(values):
            raise AssertionError(f"Sort {values}: expected {sorted(values)}, got {actual}")


def check_search(source, command):
    cases = [([], 0), ([7], 7), ([7], 8), ([3, 1, 2], 2),
             ([1, 2, 3], 4), ([7, 7, 7], 7), ([7, 7, 7], 6),
             ([-2147483648, 0, 2147483647], 2147483647)]
    for values, key in cases:
        output = run(command, input_case(source, values, key))
        if key not in values:
            if "not found" not in output.lower():
                raise AssertionError(f"Missing key {key} reported as found: {output}")
            continue
        match = re.search(r"found at index:[ \t]*(\d+)", output, re.IGNORECASE)
        if match is None:
            raise AssertionError(f"No index for key {key}: {output}")
        index = int(match.group(1))
        searched = values if source.stem == "LinearSearch" else sorted(values)
        if not 0 <= index < len(searched) or searched[index] != key:
            raise AssertionError(f"Wrong search index {index} for {values}, key={key}")


def check_source(source, build, sanitize):
    if source.suffix == ".py":
        command = [sys.executable, str(source)]
    elif source.suffix == ".java":
        # Legacy examples repeat helper names such as Sorting and Searching.
        # Compile individually: never let one overwrite another's helper classes.
        run(["javac", "-encoding", "UTF-8", "-d", str(build), str(source)])
        command = ["java", "-ea", "-cp", str(build), source.stem]
    else:
        executable = build / ("demo.exe" if os.name == "nt" else "demo")
        flags = ["-std=c99", "-Wall", "-Wextra", "-Werror", "-pedantic"]
        if sanitize:
            flags += ["-fsanitize=undefined", "-fno-sanitize-recover=all", "-g"]
        run(["cc", *flags, str(source), "-lm", "-o", str(executable)])
        command = [str(executable)]
    category = source.relative_to(ROOT).parts[0]
    if category == "Sorting-Algorithms":
        check_sort(source, command)
    elif category == "Searching Algorithms":
        check_search(source, command)
    else:
        output = run(command)
        if not output.strip():
            raise AssertionError("Demo produced no output")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", choices=("all", *LANGUAGES), default="all")
    parser.add_argument("--sanitize", action="store_true",
                        help="Enable GCC/Clang undefined-behavior checks for C")
    args = parser.parse_args()
    languages = tuple(LANGUAGES) if args.language == "all" else (args.language,)
    tools = []
    if "c" in languages:
        tools.append("cc")
    if "java" in languages:
        tools.extend(("javac", "java"))
    missing = [tool for tool in tools if shutil.which(tool) is None]
    if missing:
        parser.exit(2, "Missing required tools: " + ", ".join(missing) + "\n")
    passed, failures = Counter(), []
    with tempfile.TemporaryDirectory(prefix="algo-mastery-") as temporary:
        for category in CATEGORIES:
            for language in languages:
                sources = sorted((ROOT / category).glob("*/*" + LANGUAGES[language]))
                if not sources:
                    failures.append(f"{category}: no {language} implementations found")
                for source in sources:
                    build = Path(temporary) / str(sum(passed.values()) + len(failures))
                    build.mkdir()
                    try:
                        check_source(source, build, args.sanitize)
                    except (AssertionError, RuntimeError, OSError, subprocess.TimeoutExpired) as error:
                        failures.append(f"{source.relative_to(ROOT)}: {error}")
                    else:
                        passed[language] += 1
    for failure in failures:
        print("FAIL:", failure, file=sys.stderr)
    for language in languages:
        print(f"{language}: {passed[language]} examples passed")
    print(f"Total: {sum(passed.values())} passed, {len(failures)} failed")
    return bool(failures)


if __name__ == "__main__":
    sys.exit(main())
