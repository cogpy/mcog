#!/usr/bin/env python3
"""Validate OpenCog Maude test suite output against expected values.

Parses ``*** expect:`` annotations from the test file and compares them with
the actual results produced by Maude, verifying all equational reductions and
state-space searches.

Usage:
    python3 validate-tests.py <test-file> [maude-command]
"""

import re
import subprocess
import sys
from pathlib import Path


def parse_test_commands(test_file: str) -> list:
    """Return an ordered list of ``(cmd_type, expected)`` tuples.

    *cmd_type* is ``'red'`` or ``'search'``.
    *expected* is the annotated expected-value string, or ``None`` when no
    ``*** expect:`` comment follows the command.
    """
    lines = Path(test_file).read_text().splitlines()
    commands = []
    i = 0
    n = len(lines)

    while i < n:
        stripped = lines[i].strip()

        if stripped.startswith("red "):
            # Collect the full command — may span multiple lines up to the
            # Maude command terminator ".".
            cmd = stripped
            j = i
            while not cmd.rstrip().endswith("."):
                j += 1
                if j >= n:
                    break
                nxt = lines[j].strip()
                # Append non-empty, non-comment continuation lines.
                if nxt and not nxt.startswith("***"):
                    cmd += " " + nxt

            # Look for a "*** expect:" annotation on the next non-blank line.
            k = j + 1
            while k < n and lines[k].strip() == "":
                k += 1
            expected = None
            if k < n and lines[k].strip().startswith("*** expect:"):
                expected = lines[k].strip()[len("*** expect:"):].strip()
                if expected.endswith(" or similar"):
                    expected = expected[:-len(" or similar")]
                # Strip trailing human-readable annotation, e.g. " (lowest effectiveness)".
                # The pattern matches the last occurrence of " (text)" where text contains
                # no closing parenthesis; nested parentheses in annotations are not supported
                # (only the outermost trailing annotation group is stripped).
                expected = re.sub(r'\s+\([^)]*\)\s*$', '', expected).strip()

            commands.append(("red", expected))
            i = j + 1
            continue

        if stripped.startswith("search "):
            # Collect the full search command.
            cmd = stripped
            j = i
            while not cmd.rstrip().endswith("."):
                j += 1
                if j >= n:
                    break
                nxt = lines[j].strip()
                if nxt and not nxt.startswith("***"):
                    cmd += " " + nxt

            commands.append(("search", None))
            i = j + 1
            continue

        i += 1

    return commands


def values_match(expected: str, actual: str) -> bool:
    """Compare two result strings, treating float literals as numerically equal
    when they are within a small relative tolerance.

    Maude sometimes outputs floats in scientific notation with IEEE 754
    rounding noise (e.g. ``8.0000000000000004e-1`` instead of ``0.8``).
    This function tokenises both strings into alternating non-numeric and
    numeric segments and compares them structurally, using a relative
    tolerance of 1e-9 for numeric tokens.
    """
    if expected == actual:
        return True

    # Split each string into alternating (non-numeric, numeric) fragments.
    # The pattern handles: integers, decimals (with or without leading digit),
    # and scientific-notation literals.
    float_pat = re.compile(r'[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?')

    def tokenize(s):
        tokens = []
        pos = 0
        for m in float_pat.finditer(s):
            tokens.append(('str', s[pos:m.start()]))
            tokens.append(('num', m.group()))
            pos = m.end()
        tokens.append(('str', s[pos:]))
        return tokens

    exp_tokens = tokenize(expected)
    act_tokens = tokenize(actual)

    if len(exp_tokens) != len(act_tokens):
        return False

    for et, at in zip(exp_tokens, act_tokens):
        if et[0] != at[0]:
            return False
        if et[0] == 'str':
            # Normalise runs of whitespace so "a,b" matches "a, b" etc.
            e_norm = re.sub(r'\s+', ' ', et[1]).strip()
            a_norm = re.sub(r'\s+', ' ', at[1]).strip()
            if e_norm != a_norm:
                return False
        else:
            try:
                ev, av = float(et[1]), float(at[1])
                mag = max(abs(ev), abs(av))
                tol = 1e-9 * mag if mag > 1e-12 else 1e-12
                if abs(ev - av) > tol:
                    return False
            except ValueError:
                if et[1] != at[1]:
                    return False

    return True


def parse_maude_output(output: str) -> tuple:
    """Extract reduction results and search outcomes from Maude's output.

    Returns:
        results:      ordered list of result-value strings (one per ``reduce``).
        search_found: ordered list of bools (``True`` ↔ Solution 1 was found).
    """
    results = []
    search_found = []
    in_search = False
    found_solution = False
    in_srewrite = False   # RC2: track strategy-rewrite context to skip its results
    pending_result = None  # RC3: accumulate multi-line result terms

    for line in output.splitlines():
        stripped = line.strip()

        # RC2: Detect srewrite command — all result lines inside are ignored.
        if re.match(r"^srewrite\b", stripped):
            if pending_result is not None:
                results.append(pending_result)
                pending_result = None
            in_srewrite = True
            in_search = False
            found_solution = False
            continue

        # Start of a search command echo from Maude.
        if re.match(r"^search\s*\[", stripped):
            if pending_result is not None:
                results.append(pending_result)
                pending_result = None
            if in_search:
                search_found.append(found_solution)
                found_solution = False
            in_search = True
            in_srewrite = False
            found_solution = False
            continue

        # Reduction result: "result TYPE: VALUE"
        m = re.match(r"^result \S+:\s*(.*)", stripped)
        if m:
            if pending_result is not None:
                results.append(pending_result)
                pending_result = None
            # RC2: skip results that belong to srewrite or search blocks.
            if not in_srewrite and not in_search:
                pending_result = m.group(1).strip()
            continue

        # RC3: Continuation — raw line is indented, meaning Maude wrapped a long term.
        # pending_result is only set when we are outside search/srewrite blocks
        # (see the result-matching branch above), so indented lines here are
        # genuine continuations of a reduce result term.
        if pending_result is not None and line.startswith((' ', '\t')):
            pending_result += " " + stripped
            continue

        # Any other non-indented line flushes a pending result.
        if pending_result is not None:
            results.append(pending_result)
            pending_result = None

        # Search solved.
        if in_search and re.match(r"^Solution\s+1\b", stripped):
            found_solution = True
            continue

        # Search/srewrite ended with no solution.
        if stripped == "No solution.":
            if in_search:
                search_found.append(False)
                in_search = False
                found_solution = False
            elif in_srewrite:
                in_srewrite = False
            continue

        # Search/srewrite exhausted all solutions.
        if stripped == "No more solutions.":
            if in_search:
                search_found.append(found_solution)
                in_search = False
                found_solution = False
            elif in_srewrite:
                in_srewrite = False
            continue

    # Flush any result still being accumulated at end of output.
    if pending_result is not None:
        results.append(pending_result)

    # Handle the last search block if output ended without a closing marker.
    if in_search:
        search_found.append(found_solution)

    return results, search_found


def run_and_validate(test_file: str, maude_cmd: str = "maude") -> bool:
    """Run the test suite and validate all results.

    Returns ``True`` when every annotated assertion and every search passes.
    """
    print(f"Parsing: {test_file}")
    commands = parse_test_commands(test_file)
    red_commands = [(pos, exp) for pos, (t, exp) in enumerate(commands) if t == "red"]
    search_commands = [pos for pos, (t, _) in enumerate(commands) if t == "search"]
    annotated = sum(1 for _, e in red_commands if e is not None)

    print(
        f"Discovered {len(red_commands)} reductions "
        f"({annotated} with expected values) and {len(search_commands)} searches"
    )

    # ------------------------------------------------------------------ #
    # Run Maude                                                            #
    # ------------------------------------------------------------------ #
    print(f"\nRunning: {maude_cmd} {test_file}")
    try:
        proc = subprocess.run(
            [maude_cmd, test_file],
            capture_output=True,
            text=True,
            timeout=300,
        )
    except FileNotFoundError:
        print(f"ERROR: '{maude_cmd}' not found. Is Maude installed?")
        return False
    except subprocess.TimeoutExpired:
        print("ERROR: Maude timed out after 300 seconds.")
        return False

    output = proc.stdout + proc.stderr

    # Persist raw output for CI artifacts.
    try:
        Path("/tmp/maude-test-output.txt").write_text(output)
    except OSError:
        pass

    # ------------------------------------------------------------------ #
    # Fatal load / parse errors                                            #
    # ------------------------------------------------------------------ #
    error_lines = [
        l for l in output.splitlines()
        if re.match(r"^Error:|^parse error", l.strip())
    ]
    if error_lines:
        print("\nFATAL ERRORS in Maude output:")
        for e in error_lines:
            print(f"  {e}")
        return False

    actuals, search_found = parse_maude_output(output)

    if len(actuals) != len(red_commands):
        print(
            f"\nWARNING: Expected {len(red_commands)} result lines, "
            f"got {len(actuals)}. Output may be truncated or contain errors."
        )

    passed = 0
    failed = 0
    skipped = 0

    # ------------------------------------------------------------------ #
    # Validate equational reductions                                       #
    # ------------------------------------------------------------------ #
    print("\n=== Reduction Results ===")
    for pos, (cmd_idx, expected) in enumerate(red_commands):
        label = f"reduction {pos + 1}/{len(red_commands)}"

        if pos >= len(actuals):
            print(f"  FAIL [{label}]: no output produced")
            failed += 1
            continue

        actual = actuals[pos]

        if expected is None:
            print(f"  SKIP [{label}]: {actual[:70]}")
            skipped += 1
        elif values_match(expected, actual):
            print(f"  PASS [{label}]: {actual}")
            passed += 1
        else:
            print(f"  FAIL [{label}]: expected '{expected}', got '{actual}'")
            failed += 1

    # ------------------------------------------------------------------ #
    # Validate state-space searches                                        #
    # ------------------------------------------------------------------ #
    print("\n=== Search Results ===")
    if len(search_found) != len(search_commands):
        print(
            f"WARNING: Expected {len(search_commands)} search results, "
            f"got {len(search_found)}."
        )

    for i in range(len(search_commands)):
        label = f"search {i + 1}/{len(search_commands)}"
        if i >= len(search_found):
            print(f"  FAIL [{label}]: no result recorded")
            failed += 1
        elif search_found[i]:
            print(f"  PASS [{label}]: solution found")
            passed += 1
        else:
            print(f"  FAIL [{label}]: no solution found (expected a solution)")
            failed += 1

    # ------------------------------------------------------------------ #
    # Summary                                                              #
    # ------------------------------------------------------------------ #
    print(f"\n{'=' * 50}")
    total_checked = passed + failed
    print(
        f"Results: {passed} passed, {failed} failed, {skipped} skipped "
        f"(out of {total_checked} checked)"
    )

    if failed == 0:
        print("All tests PASSED!")
    else:
        print(f"{failed} test(s) FAILED.")

    return failed == 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <test-file> [maude-command]")
        sys.exit(1)

    _test_file = sys.argv[1]
    _maude_cmd = sys.argv[2] if len(sys.argv) > 2 else "maude"

    success = run_and_validate(_test_file, _maude_cmd)
    sys.exit(0 if success else 1)
