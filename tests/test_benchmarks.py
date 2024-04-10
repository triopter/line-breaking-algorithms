"""
These benchmark tests do not contain any correctness testing.  Please see
`test_correctness.py` for verification of correctness.
"""

import pytest
from tests.strings import ALPHA, GILBERT_SHORT, GILBERT_FULL, PREAMBLE, BLEAK_HOUSE
from tests.helpers import make_algo_id, import_algo


@pytest.mark.alpha
@pytest.mark.performance
def test_performance_alpha(benchmark, algorithm):
    if not algorithm:
        pytest.skip("no algorithm")

    in_len_out = ALPHA
    algo = import_algo(algorithm)

    # don't test our algorithms against inputs that are too long for them to perform reasonably
    if algo.break_lines.max_test_length < len(in_len_out.input.split()):
        pytest.skip("Input too long for algorithm")

    benchmark(algo.break_lines, in_len_out.input, in_len_out.max_line_length)


@pytest.mark.gilbert_short
@pytest.mark.performance
def test_performance_gilbert_short(benchmark, algorithm):
    if not algorithm:
        pytest.skip("no algorithm")

    in_len_out = GILBERT_SHORT
    algo = import_algo(algorithm)

    # don't test our algorithms against inputs that are too long for them to perform reasonably
    if algo.break_lines.max_test_length < len(in_len_out.input.split()):
        pytest.skip("Input too long for algorithm")

    benchmark(algo.break_lines, in_len_out.input, in_len_out.max_line_length)


@pytest.mark.gilbert_full
@pytest.mark.performance
def test_performance_gilbert_full(benchmark, algorithm):
    if not algorithm:
        pytest.skip("no algorithm")

    in_len_out = GILBERT_FULL
    algo = import_algo(algorithm)

    # don't test our algorithms against inputs that are too long for them to perform reasonably
    if algo.break_lines.max_test_length < len(in_len_out.input.split()):
        pytest.skip("Input too long for algorithm")

    benchmark(algo.break_lines, in_len_out.input, in_len_out.max_line_length)


@pytest.mark.preamble
@pytest.mark.performance
def test_performance_preamble(benchmark, algorithm):
    if not algorithm:
        pytest.skip("no algorithm")

    in_len_out = PREAMBLE
    algo = import_algo(algorithm)

    # don't test our algorithms against inputs that are too long for them to perform reasonably
    if algo.break_lines.max_test_length < len(in_len_out.input.split()):
        pytest.skip("Input too long for algorithm")

    benchmark(algo.break_lines, in_len_out.input, in_len_out.max_line_length)


@pytest.mark.bleak_house
@pytest.mark.performance
def test_performance_bleak_house(benchmark, algorithm):
    if not algorithm:
        pytest.skip("no algorithm")

    in_len_out = BLEAK_HOUSE
    algo = import_algo(algorithm)

    # don't test our algorithms against inputs that are too long for them to perform reasonably
    if algo.break_lines.max_test_length < len(in_len_out.input.split()):
        pytest.skip("Input too long for algorithm")

    benchmark(algo.break_lines, in_len_out.input, in_len_out.max_line_length)
