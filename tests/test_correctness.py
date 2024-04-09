"""
Tests that our algorithms have the correct output for given known inputs/line lengths.
"""

import pytest
from importlib import import_module
from pathlib import Path
from tests.strings import INPUTS_LENGTHS_OUTPUTS

REPO_ROOT = Path(__file__).parent.parent


def make_algo_id(algo_name):
    return algo_name


@pytest.fixture(params=REPO_ROOT.joinpath("algorithms").glob("*.py"), ids=make_algo_id)
def algorithm(request):
    print(request.param)
    if (request.param.name) == "__init__.py":
        return None
    return import_module(f"algorithms.{request.param.stem}")


def make_test_id(case):
    return case.name


def calculate_penalty(lines, max_length):
    return sum([(max_length - len(line)) ** 2 for line in lines])


@pytest.mark.parametrize("in_len_out", INPUTS_LENGTHS_OUTPUTS, ids=make_test_id)
def test_correctness(algorithm, in_len_out):
    if not algorithm:
        return

    # don't test our algorithms against inputs that are too long for them to perform reasonably
    if algorithm.break_lines.max_test_length < len(in_len_out.input.split()):
        return

    print(
        algorithm.__file__,
        in_len_out,
        "\\n".join(algorithm.break_lines(in_len_out.input, in_len_out.max_line_length)),
    )

    lines = algorithm.break_lines(in_len_out.input, in_len_out.max_line_length)
    expected = in_len_out.output.split("\n")

    assert calculate_penalty(lines, in_len_out.max_line_length) == calculate_penalty(
        expected, in_len_out.max_line_length
    )

    # assert lines == expected
