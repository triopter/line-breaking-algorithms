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

The previous way ["dynamic programming"] can be sped up even further: 
the length offsets used to calculate any line length in constant time can 
easily be pre-processed in O(n), rather than O(n ^ 2), and there is no point 
in putting ever more words on a line once it reaches the allowed width. The 
performance then improves down to O(n * width).

This is exactly the same result as if the text was thought of as a 
(topologically sorted) directed acyclic graph, with the nodes and arcs
representing words and breaks, respectively. By substituting the penalties for
the weights, the problem becomes the one of finding the shortest path which is 
known to be solvable in linear time. Note that the number of edges remains 
O(n * width).
"""

"""
Noemi's thoughts: The building-backwards approach presumably suffers from the 
same potential issues as the dynamic programming algo.  (This is essentially 
that exact algo with some unnecessary work excised.)
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

    # Loop through potential lines.  This loop works as follows:
    # Start with a line of just the first word of the text
    # The inner loop moves the last word of the current line forward
    # The outer loop moves the first word of the current line forward, and resets the last word to make a single-word line
    for line_start in range(word_count):
        line_end = line_start + 1

        while line_end <= word_count:
            # line length is the length of all the words in the line
            # (first char index of the last word in the line minus char index of the first word of the line)
            # plus the number of spaces (which is the number of words in the line, minus one)
            line_length = (
                word_starts[line_end]
                - word_starts[line_start]
                + line_end
                - line_start
                - 1
            )

            # This potential line (and any after it in the inner loop) is too long; don't bother saving it
            if line_length > max_length:
                break

            # this line's penalty is the penalty for the best option so far for the line start plus the square of the extra space for the line
            line_penalty = min_penalties[line_start] + (max_length - line_length) ** 2

            # Unless the line is too long, it's the best option we've found so far for a line that would end at the current ending index
            # So save this starting word as a potential break point for this ending word
            if line_penalty < min_penalties[line_end]:
                min_penalties[line_end] = line_penalty
                optimal_start_for_end[line_end] = line_start

            line_end += 1

    # As with the dynamic programming approach, we assemble our lines by working backwards from the last word of the text
    lines = []
    line_end = word_count
    while line_end > 0:
        # We find the best starting point for the line ending with the current word
        line_start = optimal_start_for_end[line_end]
        # Make that line
        lines.append(" ".join(words[line_start:line_end]))
        # Then move to look at what the previous line would be
        line_end = line_start
    lines.reverse()
    return lines
