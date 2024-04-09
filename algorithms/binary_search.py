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
Noemi's notes:
I haven't entirely figured out how this algorithm operates -- in particular, how the 
queue (currently named `lines_to_test`) is used.

Note that the original version of this algorithm as of 2024-04-08 gave incorrect output 
for at least one sample input:

In:
To sit in solemn silence on a dull, dark dock
max_length: 16

Expected: 
To sit in solemn
silence on a
dull, dark dock

Actual:
To sit in
solemn silence 
on a dull,
dark dock

Juraj quickly identified the error (off-by-one in `find_best_end`).  The version
in this file now produces expected output for all test cases in the repo.
"""


from collections import deque


def break_lines(text, max_length):
    words = text.split()
    word_count = len(words)

    # Here we store the index of the character (relative to the whole text) that each word starts at, minus any spaces
    word_starts = [0]
    for maybe_break_before in words:
        # Each word starts at the previous word's start index plus its own length
        word_starts.append(word_starts[-1] + len(maybe_break_before))

    min_penalties = [0] * (word_count + 1)
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

    # binary search here
    # We're binary-searching between new_start and current_start
    def find_best_end(new_start, current_start):
        # originally new_start + 1, gave incorrect output
        leftmost_possible_end = new_start
        rightmost_possible_end = word_count

        # Iterate until we've run out of words to check
        # We're using a binary partitioning (at median_end) looking for a line end (best_possible_end)
        # at which the new line start would be better than the current line start
        while leftmost_possible_end < rightmost_possible_end:
            median_end = (leftmost_possible_end + rightmost_possible_end) // 2

            # Note that due to too-long-line penalty scaling, this comparison will return True
            # if both lines are too long but the one on the right is too long by more than the one on the left
            # but false if the one on the left is too long by more than the one on the right
            if calculate_penalty(new_start, median_end) <= calculate_penalty(
                current_start, median_end
            ):
                rightmost_possible_end = median_end
            else:
                leftmost_possible_end = median_end + 1

        # Check whether we actually found a line end at which the new start would be better than the current start
        if calculate_penalty(new_start, rightmost_possible_end) <= calculate_penalty(
            current_start, rightmost_possible_end
        ):
            # if we found one, return it
            return rightmost_possible_end

        # originally new_start + 2, gave incorrect output
        return new_start + 1

    # A queue (list with performance advantages) of (start, end) tuples
    # All lines in lines_to_test are always valid lines less than max_length
    # This loop discards any that are suboptimal -- I still haven't figured out exactly how
    lines_to_test = deque([(0, 1)])
    # Each iteration of this loop tests the current word as a potential line ending
    # (word to break before, not the last word) for the next line
    for maybe_break_before in range(1, word_count + 1):

        maybe_start = lines_to_test[0][0]

        # if the penalty for a one-word line ending at the current word
        # is lower than/equal to the penalty for a line running from the first potential line start
        # to the current word -- which will be true only if the latter is too long, I think
        # and also on the first iteration (or any other iteration) when the first potential start is the prev word
        if calculate_penalty(
            maybe_break_before - 1, maybe_break_before
        ) <= calculate_penalty(maybe_start, maybe_break_before):
            # Then the best potential line we have for this line end is the one-word line, I think
            min_penalties[maybe_break_before] = calculate_penalty(
                maybe_break_before - 1, maybe_break_before
            )
            # and the best start word so far for this end word is the one-word line start
            optimal_start_for_end[maybe_break_before] = maybe_break_before - 1
            # reset the queue to just a two-word line containing this word and the one after it
            lines_to_test.clear()
            # on the next iteration,
            lines_to_test.append((maybe_break_before - 1, maybe_break_before + 1))

        # A two-word line line is better than a one-word line
        else:
            # So save it as the best line we know for this line end
            min_penalties[maybe_break_before] = calculate_penalty(
                maybe_start, maybe_break_before
            )
            optimal_start_for_end[maybe_break_before] = maybe_start

            # How this loop works:
            # We're comparing two potential lines.  The one on the left side of the comparison
            # has its start set to the word before the current word, and its end
            # set to the end of last line in our list of potential lines.
            # The one on the right side of the comparison is the most recently added potential line.
            # (On the first iteration, this potential line will be set to a one-word line at the start of the text.)
            # If the line on the left is a better fit than the one on the right,
            # we eliminate the one on the right from our list of potential lines and try again.
            #
            # This compares two lines ending in the same word.  If the one starting with our current potential start
            # is better than the one already queued, there's no point in saving the one on the queue
            while calculate_penalty(
                maybe_break_before - 1, lines_to_test[-1][1]
            ) <= calculate_penalty(lines_to_test[-1][0], lines_to_test[-1][1]):
                # our last attempt at producing a next line was no good.  discard it
                lines_to_test.pop()

            # Here we add a potential line that's the best possible line starting with the word before our currently considered line break
            lines_to_test.append(
                (
                    maybe_break_before - 1,
                    # after removing unnecessary increment inside function, no decrement needed here
                    find_best_end(maybe_break_before - 1, lines_to_test[-1][0]),
                )
            )

            # check if current word is the end of our second (last?) line in the test list
            if maybe_break_before + 1 == lines_to_test[1][1]:
                # If so, the line we just added is the correct next line.  We can discard the previous line's queue data
                # and make this the previous line record.
                lines_to_test.popleft()
            else:
                # Extend the first line in the test list by one word to the right
                lines_to_test[0] = (lines_to_test[0][0], (lines_to_test[0][1] + 1))

    # assemble lines from back to front again
    formatted_lines = []
    maybe_break_before = word_count
    while maybe_break_before > 0:
        start_index = optimal_start_for_end[maybe_break_before]
        formatted_lines.append(" ".join(words[start_index:maybe_break_before]))
        maybe_break_before = start_index
    formatted_lines.reverse()

    return formatted_lines
