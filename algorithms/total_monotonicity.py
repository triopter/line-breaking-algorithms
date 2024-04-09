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

import math


def break_lines(text, max_length):
    words = text.split()
    word_count = len(words)

    # Here we store the index of the character (relative to the whole text) that each word starts at, minus any spaces
    word_starts = [0]
    for word in words:
        # Each word starts at the previous word's start index plus its own length
        word_starts.append(word_starts[-1] + len(word))

    min_penalties = [0] + [10**20] * word_count
    optimal_start_for_end = [0] * (word_count + 1)

    def calculate_penalty(first_word, break_before):
        # line length is the length of all the words in the line
        # (first char index of the last word in the line minus char index of the first word of the line)
        # plus the number of spaces (which is the number of words in the line, minus one)
        line_length = (
            word_starts[break_before]
            - word_starts[first_word]
            + break_before
            - first_word
            - 1
        )

        # here instead of a standard "really big" number for too-long lines,
        # we're scaling them by just how much too big they are
        if line_length > max_length:
            return 10**10 * (line_length - max_length)

        return min_penalties[first_word] + (max_length - line_length) ** 2

    def smawk(start_words, end_words):
        possible_starts = []
        start_ix = 0

        # Iterate through rows
        while start_ix < len(start_words):
            if possible_starts:
                # find column corresponding to the number of potential line starts we've identified so far
                end_word = end_words[len(possible_starts) - 1]

                # if our furthest line start is a better fit than the one at this row index
                if calculate_penalty(possible_starts[-1], end_word) < calculate_penalty(
                    start_words[start_ix], end_word
                ):
                    # and if we still have more starts to look at
                    if len(possible_starts) < len(end_words):
                        # add this as a potential start
                        possible_starts.append(start_words[start_ix])
                    start_ix += 1
                else:
                    # the last potential start is irrelevant
                    # try again with the previous one
                    possible_starts.pop()

            # we need to populate our line starts -- the potential one we have is going to be the only and thus best one so far
            else:
                possible_starts.append(start_words[start_ix])
                start_ix += 1

        start_words = possible_starts

        # if we've got at least two items, add any potential starts with a step value of two starting at the second item?  why?
        if len(end_words) > 1:
            smawk(start_words, end_words[1::2])

        start_ix = end_ix = 0
        # Iterate through our potential line starts and ends until we've exhausted them
        while end_ix < len(end_words):
            if end_ix + 1 < len(end_words):
                end = optimal_start_for_end[end_words[end_ix + 1]]
            else:
                # last potential start value
                end = start_words[-1]

            line_cost = calculate_penalty(start_words[start_ix], end_words[end_ix])

            # if it's the best start we've found so far for this end, save it
            if line_cost < min_penalties[end_words[end_ix]]:
                min_penalties[end_words[end_ix]] = line_cost
                optimal_start_for_end[end_words[end_ix]] = start_words[start_ix]

            # if the start hasn't run past the end, increment it
            if start_words[start_ix] < end:
                start_ix += 1
            # if it has, increment the end by two (why two?)
            else:
                end_ix += 2

    total_words = word_count + 1
    iteration_index = 0
    current_offset = 0

    while True:
        # the number of potential last words in the line, doubles until we hit the text length
        last_word_to_check = min(total_words, 2 ** (iteration_index + 1))
        # I believe this is moving at a diagonal along the start/end matrix
        # We can't start a line with a word after this one or end a line with a word before it
        current_edge = 2**iteration_index + current_offset

        # populates the min penalties
        smawk(
            # list of potential start words
            range(0 + current_offset, current_edge),
            # list of potential end words
            range(current_edge, last_word_to_check + current_offset),
        )

        best_cost = min_penalties[last_word_to_check - 1 + current_offset]

        for start_ix in range(2**iteration_index, last_word_to_check - 1):
            potential_cost = calculate_penalty(
                start_ix + current_offset, last_word_to_check - 1 + current_offset
            )
            if potential_cost <= best_cost:
                total_words -= start_ix
                iteration_index = 0
                current_offset += start_ix
                break
        else:
            if last_word_to_check == total_words:
                break
            iteration_index = iteration_index + 1

    lines = []
    current_index = word_count
    while current_index > 0:
        start_index = optimal_start_for_end[current_index]
        lines.append(" ".join(words[start_index:current_index]))
        current_index = start_index
    lines.reverse()
    return lines


# skip tests with inputs more than this number of words long
break_lines.max_test_length = math.inf
