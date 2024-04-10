"""
Tests that our algorithms have the correct output for given known inputs/line lengths.
"""

import pytest
from pathlib import Path
from tests.helpers import import_algo
from tests.strings import INPUTS_LENGTHS_OUTPUTS


def make_test_id(case):
    return case.name


# total penalty for the entire text (sum of squares of differences between line lengths and target length)
def calculate_penalty(lines, max_length):
    return sum([(max_length - len(line)) ** 2 for line in lines])


@pytest.mark.parametrize("in_len_out", INPUTS_LENGTHS_OUTPUTS, ids=make_test_id)
@pytest.mark.correctness
def test_correctness(algorithm, in_len_out):
    if not algorithm:
        pytest.skip("no algorithm")

    algo = import_algo(algorithm)

    # don't test our algorithms against inputs that are too long for them to perform reasonably
    if algo.break_lines.max_test_length < len(in_len_out.input.split()):
        pytest.skip("Input too long for algorithm")

    lines = algo.break_lines(in_len_out.input, in_len_out.max_line_length)
    expected = in_len_out.output.split("\n")

    # sometimes two variations are equally good, so instead of confirming the algos give
    # the exact same output, we confirm they give equivalently good output
    assert calculate_penalty(lines, in_len_out.max_line_length) == calculate_penalty(
        expected, in_len_out.max_line_length
    )
