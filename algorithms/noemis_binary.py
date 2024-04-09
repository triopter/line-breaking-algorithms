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

"""
Noemi's Notes:

Because I was getting incorrect output from the original binary search algorithm,
I ended up implementing this based partly on the shortest_path algorithm and
partly on the binary one.

I believe this algo could be improved further by calculating the last line first 
and then moving back by an entire line instead of a single word.
"""


def break_lines(text, max_length):
    words = text.split()
    word_count = len(words)

    # Here we store the index of the character (relative to the whole text) that each word starts at, minus any spaces
    word_starts = [0]
    for word in words:
        # Each word starts at the previous word's start index plus its own length
        word_starts.append(word_starts[-1] + len(word))

    # Using "penalties" again based on the squares of how much shorter each line is than the max.
    # As with the "dynamic programming" approach, here we're storing a list of them, one for each word
    # first one is set to zero and the rest are set to a prohibitively high value
    # The value at each index represents the lowest penalty we've found so far for any line ENDING at that word
    # Each word's min penalty is the value at its index
    min_penalties = [0] + [10**20] * word_count
    # For each word at index i, the value at i in this list will store the optimal starting word index for a line ENDING at word i
    optimal_start_for_end = [0] * (word_count + 1)

    def calculate_line_penalty(first_word, break_before):
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

        penalty = min_penalties[first_word] + (max_length - line_length) ** 2
        min_penalties[first_word] = min(min_penalties[first_word], penalty)
        return penalty

    def get_best_line_start(line_end):
        # line_end will always be >= 1
        # the best start is somewhere between beginning of text and the word before the ending one
        lower_bound = 0
        upper_bound = line_end

        # on each iteration, compare median start to median start plus one
        # to determine which side of the median the min is on
        # knowing that in a concave function, the answer will always be to one side or the other, or the median itself
        while lower_bound < upper_bound:
            median_start = (lower_bound + upper_bound) // 2
            print(
                "line, low, up, med", line_end, lower_bound, upper_bound, median_start
            )
            print(
                "end, low, up, med",
                words[line_end - 1],
                words[lower_bound],
                words[upper_bound - 1],
                words[median_start],
            )
            print(
                "pen",
                calculate_line_penalty(median_start, line_end),
                calculate_line_penalty(median_start + 1, line_end),
            )

            # Note that median_start will always be less than upper_bound, so adding one will make it at most equal to upper bound
            # if penalty for median_start is lower, then our min penalty is on the left hand side of our range
            if calculate_line_penalty(median_start, line_end) <= calculate_line_penalty(
                median_start + 1, line_end
            ):
                upper_bound = median_start
            else:
                lower_bound = median_start + 1

        print("final bound", lower_bound, upper_bound)
        # this should converge on our result, with both bounds being equal
        return lower_bound

    def get_best_line_end(line_start):
        # line_end will always be >= 1
        # the best start is somewhere between beginning of text and the word before the ending one
        lower_bound = line_start + 1
        upper_bound = word_count

        # on each iteration, compare median end to median end plus one
        # to determine which side of the median the min is on
        # knowing that in a concave function, the answer will always be to one side or the other, or the median itself
        while lower_bound < upper_bound:
            median_end = (lower_bound + upper_bound) // 2
            print(
                "line, low, up, med", line_start, lower_bound, upper_bound, median_end
            )
            print(
                "pen",
            )

            # Note that median_end will always be less than upper_bound, so adding one will make it at most equal to upper bound
            # if penalty for median_end is lower, then our min penalty is on the left hand side of our range
            if calculate_line_penalty(line_start, median_end) <= calculate_line_penalty(
                line_start, median_end + 1
            ):
                upper_bound = median_end
            else:
                lower_bound = median_end + 1
        # this should converge on our result, with both bounds being equal
        return lower_bound

    # This loop works as follows:
    # Start at the first word of text
    # Binary search the preceding words for the one with the optimal line length to break before
    # The outer loop moves the last word of the current line forward
    for line_end in range(1, word_count + 1):
        print(line_end)
        best_start = get_best_line_start(line_end) + 1
        optimal_start_for_end[line_end] = best_start
        print("best", best_start, line_end, words[best_start:line_end])

    # As with the dynamic programming approach, we assemble our lines by working backwards from the last word of the text
    lines = []
    line_end = word_count
    from pprint import pprint

    print(line_end, [(end, start) for end, start in enumerate(optimal_start_for_end)])
    pprint([(end, words[start:end]) for end, start in enumerate(optimal_start_for_end)])

    while line_end > 1:
        #     # We find the best starting point for the line ending with the current word
        line_start = optimal_start_for_end[line_end]
        print(line_start, line_end)
        #     # Make that line
        lines.append(" ".join(words[line_start:line_end]))
        #     # Then move to look at what the previous line would be
        line_end = line_start
    lines.reverse()
    print(lines)

    return lines
