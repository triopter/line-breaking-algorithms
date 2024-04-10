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
