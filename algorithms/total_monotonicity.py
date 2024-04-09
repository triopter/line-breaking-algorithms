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

Each iteration of the dynamic programming scheme can also be seen as 
filling in a matrix, where a cell adds up the least overall cost to 
a subproblem (a column minimum) and a penalty. A concave weight function 
implies that the matrix is totally monotone and in 1987 Shor, Moran, Aggarwal, 
Wilber and Klawe[1] devised an algorithm which finds the row maxima of such 
matrix in linear time. Even though SMAWK can be modified to find 
column minima instead, it is not possible to apply it directly to this 
"on-line" matrix as it might try to evaluate a not "available" cell, i.e. 
a cell dependent on some yet unknown column minimum. However, Wilber 
came up with an algorithm in 1988[2] which "pretends" to know the minima and 
still runs in O(n) time. An "ordered" algorithm which obeys the availability 
of the matrix as presented by Aggarwal and Tokuyama in 1998[3] follows.

[1] A. Aggarwal, M. M. Klawe, S. Moran, P. Shor, R. Wilber. Geometric 
Applications of a Matrix-Searching Algorithm. Algorithmica 2, 1987.

[2] R. Wilber. The Concave Least-Weight Subsequence Problem Revisited. 
Journal of Algorithms 9, 1988.

[3] A. Aggarwal, T. Tokuyama. Consecutive interval query and dynamic 
programming on intervals. Discrete Applied Mathematics 85, 1998.
"""


def break_lines(text, max_length):
    words = text.split()
    word_count = len(words)
    word_offsets = [0]
    for word in words:
        word_offsets.append(word_offsets[-1] + len(word))

    minima_costs = [0] + [10**20] * word_count
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
            return 10**10 * (line_width - max_length)
        return minima_costs[start_index] + (max_length - line_width) ** 2

    def smawk_algorithm(rows, columns):
        stack = []
        row_index = 0
        while row_index < len(rows):
            if stack:
                column = columns[len(stack) - 1]
                if calculate_cost(stack[-1], column) < calculate_cost(
                    rows[row_index], column
                ):
                    if len(stack) < len(columns):
                        stack.append(rows[row_index])
                    row_index += 1
                else:
                    stack.pop()
            else:
                stack.append(rows[row_index])
                row_index += 1
        rows = stack

        if len(columns) > 1:
            smawk_algorithm(rows, columns[1::2])

        row_index = column_index = 0
        while column_index < len(columns):
            if column_index + 1 < len(columns):
                end_row = optimal_breaks[columns[column_index + 1]]
            else:
                end_row = rows[-1]
            current_cost = calculate_cost(rows[row_index], columns[column_index])
            if current_cost < minima_costs[columns[column_index]]:
                minima_costs[columns[column_index]] = current_cost
                optimal_breaks[columns[column_index]] = rows[row_index]
            if rows[row_index] < end_row:
                row_index += 1
            else:
                column_index += 2

    total_words = word_count + 1
    iteration_index = 0
    current_offset = 0
    while True:
        range_end = min(total_words, 2 ** (iteration_index + 1))
        current_edge = 2**iteration_index + current_offset
        smawk_algorithm(
            range(0 + current_offset, current_edge),
            range(current_edge, range_end + current_offset),
        )
        current_minima = minima_costs[range_end - 1 + current_offset]
        for column_index in range(2**iteration_index, range_end - 1):
            potential_cost = calculate_cost(
                column_index + current_offset, range_end - 1 + current_offset
            )
            if potential_cost <= current_minima:
                total_words -= column_index
                iteration_index = 0
                current_offset += column_index
                break
        else:
            if range_end == total_words:
                break
            iteration_index = iteration_index + 1

    lines = []
    current_index = word_count
    while current_index > 0:
        start_index = optimal_breaks[current_index]
        lines.append(" ".join(words[start_index:current_index]))
        current_index = start_index
    lines.reverse()
    return lines
