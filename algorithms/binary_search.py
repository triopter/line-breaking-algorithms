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

    # Here we store the index of the character (relative to the whole text) that each word starts at, minus any spaces
    word_starts = [0]
    for current_word in words:
        # Each word starts at the previous word's start index plus its own length
        word_starts.append(word_starts[-1] + len(current_word))

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
        lowest_possible_end, best_possible_end = new_start + 1, word_count

        # Iterate until we've run out of words to check
        # We're using a binary partitioning (at median_end) looking for a line end (best_possible_end)
        # at which the new line start would be better than the current line start
        while lowest_possible_end < best_possible_end:
            median_end = (lowest_possible_end + best_possible_end) // 2

            # Note that due to too-long-line penalty scaling, this comparison will return True
            # if both lines are too long but the one on the right is too long by more than the one on the left
            # but false if the one on the left is too long by more than the one on the right
            if calculate_penalty(new_start, median_end) <= calculate_penalty(
                current_start, median_end
            ):
                best_possible_end = median_end
            else:
                lowest_possible_end = median_end + 1

        # Check whether we actually found a line end at which the new start would be better than the current start
        if calculate_penalty(new_start, best_possible_end) <= calculate_penalty(
            current_start, best_possible_end
        ):
            # if we found one, return it
            return best_possible_end

        # Otherwise, I think this is telling us to try a 2-word line?  Not sure why +2.
        return new_start + 2

    # A queue (list with performance advantages) of (start, end) tuples
    # I believe that [0][0] always represents the leftmost word we could possibly use for a line ending in the current word
    # this queue is only ever 1 or two items long
    lines_to_test = deque([(0, 1)])
    # Each iteration of this loop tests the current word as a potential line ending for the next line
    #
    for current_word in range(1, word_count + 1):
        print("testing", lines_to_test, current_word)

        maybe_start = lines_to_test[0][0]

        # if the penalty for a one-word line ending at the current word
        # is lower than/equal to the penalty for a line running from the first potential line start
        # to the current word -- which will be true only if the latter is too long, I think
        # and also on the first iteration (or any other iteration) when the first potential start is the prev word
        if calculate_penalty(current_word - 1, current_word) <= calculate_penalty(
            maybe_start, current_word
        ):
            print("one word is best:", words[current_word - 1])
            # Then the best potential line we have for this line end is the one-word line, I think
            min_penalties[current_word] = calculate_penalty(
                current_word - 1, current_word
            )
            # and the best start word so far for this end word is the one-word line start
            optimal_start_for_end[current_word] = current_word - 1
            # reset the queue to just a two-word line containing this word and the one after it
            lines_to_test.clear()
            # on the next iteration,
            lines_to_test.append((current_word - 1, current_word + 1))

        # A two-word line line is better than a one-word line
        else:
            # So save it as the best line we know for this line end
            min_penalties[current_word] = calculate_penalty(maybe_start, current_word)
            optimal_start_for_end[current_word] = maybe_start

            # How this loop works:
            # We're comparing two potential lines.  The one on the left side of the comparison
            # has its start set to the word before the current word, and its end
            # set to the end of last line in our list of potential lines.
            # The one on the right side of the comparison is the most recently added potential line.
            # (On the first iteration, this potential line will be set to a one-word line at the start of the text.)
            # If the line on the left is a better fit than the one on the right,
            # we eliminate the one on the right from our list of potential lines and try again.
            while calculate_penalty(
                current_word - 1, lines_to_test[-1][1]
            ) <= calculate_penalty(lines_to_test[-1][0], lines_to_test[-1][1]):
                lines_to_test.pop()

            # Now we take as our bounds the word before the line end
            # And the best line end we can find for the line starting with the word after the current line end
            lines_to_test.append(
                (
                    current_word - 1,
                    find_best_end(current_word - 1, lines_to_test[-1][0]),
                )
            )

            # check if current word is the end of our second (last?) line in the test list
            if current_word + 1 == lines_to_test[1][1]:
                # If so, the first line in the test list is no longer relevant
                lines_to_test.popleft()
            else:
                # Extend the first line in the test list by one word to the right
                lines_to_test[0] = (lines_to_test[0][0], (lines_to_test[0][1] + 1))

    # assemble lines from back to front again
    formatted_lines = []
    current_word = word_count
    import pprint

    pprint.pprint([(end, start) for end, start in enumerate(optimal_start_for_end)])
    while current_word > 0:
        start_index = optimal_start_for_end[current_word]
        formatted_lines.append(" ".join(words[start_index:current_word]))
        current_word = start_index
    formatted_lines.reverse()

    return formatted_lines
