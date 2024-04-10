# line-breaking-algorithms

Investigation of line-breaking algorithms demonstrated by Juraj Sukop at 
https://xxyxyz.org/line-breaking/ .

Algorithms are discussed on that page in the following order:

1. [Brute force](algorithms/brute_force.py)
1. ["Dynamic programming"](algorithms/dynamic_programming.py)
1. [Shortest path](algorithms/shortest_path.py)
1. [Binary Search](algorithms/binary_search.py)
1. [Total Monotonicity](algorithms/total_monotonicity.py)
1. [Divide & Conquer](algorithms/divide_and_conquer.py)


# Performance Analysis

For the longest texts/line lengths (the 750+ word Bleak House excerpt), the Divide & Conquer 
algorithm tends to be most performant, with Shortest Path the runner up.

For shorter texts/line lengths (the alphabet sample or the single line Gilbert & Sullivan sample), 
the Shortest Path algorithm is most performant.

The full Gilbert & Sullivan and the Preamble to the US Constitution seem to sit on the cusp of those 
cases, with Shortest Path and Divide & Conquer offering trade-offs.


# Testing

Performance and correctness tests are handled separately.

```bash
$ python -m pytest -m correctness
$ python -m pytest -m performance --benchmark-group-by=func
```

Performance tests can also be run for only a specific test input.  Markers are defined in [pytest.ini](pytest.ini):

```bash
$ python -m pytest -m preamble
```

Note when comparing performance across different inputs that pytest-benchmark uses different
scales for each input if you either group them or test only a single input.

