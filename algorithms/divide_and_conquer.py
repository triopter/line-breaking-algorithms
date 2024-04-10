# Copyright (c) 2014, Juraj Sukop
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
# OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.


"""
Via https://xxyxyz.org/line-breaking/:

One additional option is to replace the preceding [total_monotonicity.py] 
SMAWK routine and its fairly large constant factor by a simple divide & conquer 
monotone matrix search. The complexity will drop back to O(n * log n) but for 
smaller problem instances it may actually run faster than the asymptotically 
superior approach.
"""

"""
Noemi's notes:
Understanding this one to add comments or update the variable names beyond 
what an LLM is capable of is also out of scope due to time and energy constraints.
Clarifying PRs welcome here as well.
"""


import math


def break_lines(text, max_length):
    words = text.split()
    word_count = len(words)
    word_offsets = [0]
    for word in words:
        word_offsets.append(word_offsets[-1] + len(word))

    minimum_costs = [0] + [10**20] * word_count
    optimal_breaks = [0] * (word_count + 1)

    def calculate_cost(start_index, end_index):
        line_width = (
            word_offsets[end_index]
            - word_offsets[start_index]
            + end_index
            - start_index
            - 1
        )
        if line_width > max_length:
            return 10**10
        return minimum_costs[start_index] + (max_length - line_width) ** 2

    def search(start_range_begin, end_range_begin, start_range_end, end_range_end):
        search_stack = [
            (start_range_begin, end_range_begin, start_range_end, end_range_end)
        ]
        while search_stack:
            start_range_begin, end_range_begin, start_range_end, end_range_end = (
                search_stack.pop()
            )
            if end_range_begin < end_range_end:
                middle_index = (end_range_begin + end_range_end) // 2
                for current_index in range(start_range_begin, start_range_end):
                    current_cost = calculate_cost(current_index, middle_index)
                    if current_cost <= minimum_costs[middle_index]:
                        minimum_costs[middle_index] = current_cost
                        optimal_breaks[middle_index] = current_index
                search_stack.append(
                    (
                        optimal_breaks[middle_index],
                        middle_index + 1,
                        start_range_end,
                        end_range_end,
                    )
                )
                search_stack.append(
                    (
                        start_range_begin,
                        end_range_begin,
                        optimal_breaks[middle_index] + 1,
                        middle_index,
                    )
                )

    total_words = word_count + 1
    iteration_index = 0
    current_offset = 0
    while True:
        range_limit = min(total_words, 2 ** (iteration_index + 1))
        current_edge = 2**iteration_index + current_offset
        search(
            0 + current_offset, current_edge, current_edge, range_limit + current_offset
        )
        best_cost = minimum_costs[range_limit - 1 + current_offset]
        for current_index in range(2**iteration_index, range_limit - 1):
            potential_cost = calculate_cost(
                current_index + current_offset, range_limit - 1 + current_offset
            )
            if potential_cost <= best_cost:
                total_words -= current_index
                iteration_index = 0
                current_offset += current_index
                break
        else:
            if range_limit == total_words:
                break
            iteration_index += 1

    lines = []
    current_word_index = word_count
    while current_word_index > 0:
        start_index = optimal_breaks[current_word_index]
        lines.append(" ".join(words[start_index:current_word_index]))
        current_word_index = start_index
    lines.reverse()
    return lines


# skip tests with inputs more than this number of words long
break_lines.max_test_length = math.inf
