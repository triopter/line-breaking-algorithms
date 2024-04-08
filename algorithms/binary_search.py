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

The method using "dynamic programming" can be written as two nested loops: 
the outer one iterates over every word and the inner one searches for the most 
suitable break. Hirschberg and Larmore showed in 1987 an algorithm which is 
able to use binary search instead of the inner loop in the case the weight 
function is "concave". It turns out that the penalty discussed thus far can be 
made to satisfy this property by handling the "infinities" slightly differently, 
giving an overall time of O(n * log n). A similar algorithm due to Galil and 
Giancarlo from 1989[1] is given below.

The concave property says: w(i, j) + w(i', j') <= w(i', j) + w(i, j'), 
where i < i' < j < j'.

[1] Z. Galil, R. Giancarlo. Speeding up dynamic programming with applications 
to molecular biology. Theoretical Computer Science 64, 1989.
"""


from collections import deque


def break_lines(text, max_length):
    words = text.split()
    word_count = len(words)
    word_offsets = [0]
    for word in words:
        word_offsets.append(word_offsets[-1] + len(word))

    line_minima = [0] * (word_count + 1)
    line_breaks = [0] * (word_count + 1)

    def calculate_penalty(start_index, end_index):
        line_width = (
            word_offsets[end_index]
            - word_offsets[start_index]
            + end_index
            - start_index
            - 1
        )
        if line_width > max_length:
            return 10**10 * (line_width - max_length)
        return line_minima[start_index] + (max_length - line_width) ** 2

    def find_best_break(previous_break, current_break):
        lower_bound, upper_bound = previous_break + 1, word_count
        while lower_bound < upper_bound:
            middle = (lower_bound + upper_bound) // 2
            if calculate_penalty(previous_break, middle) <= calculate_penalty(
                current_break, middle
            ):
                upper_bound = middle
            else:
                lower_bound = middle + 1
        if calculate_penalty(previous_break, upper_bound) <= calculate_penalty(
            current_break, upper_bound
        ):
            return upper_bound
        return previous_break + 2

    break_queue = deque([(0, 1)])
    for current_index in range(1, word_count + 1):
        previous_break = break_queue[0][0]
        if calculate_penalty(current_index - 1, current_index) <= calculate_penalty(
            previous_break, current_index
        ):
            line_minima[current_index] = calculate_penalty(
                current_index - 1, current_index
            )
            line_breaks[current_index] = current_index - 1
            break_queue.clear()
            break_queue.append((current_index - 1, current_index + 1))
        else:
            line_minima[current_index] = calculate_penalty(
                previous_break, current_index
            )
            line_breaks[current_index] = previous_break
            while calculate_penalty(
                current_index - 1, break_queue[-1][1]
            ) <= calculate_penalty(break_queue[-1][0], break_queue[-1][1]):
                break_queue.pop()
            break_queue.append(
                (
                    current_index - 1,
                    find_best_break(current_index - 1, break_queue[-1][0]),
                )
            )
            if current_index + 1 == break_queue[1][1]:
                break_queue.popleft()
            else:
                break_queue[0] = break_queue[0][0], (break_queue[0][1] + 1)

    formatted_lines = []
    current_index = word_count
    while current_index > 0:
        start_index = line_breaks[current_index]
        formatted_lines.append(" ".join(words[start_index:current_index]))
        current_index = start_index
    formatted_lines.reverse()
    return formatted_lines
