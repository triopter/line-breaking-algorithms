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
via https://xxyxyz.org/line-breaking/:
The deficiency of [the brute force approach] lies in that it repeatedly solves the same subproblems. 
Yet suppose there was an optimal configuration of lines. Plucking off its last line would still 
keep the layout optimal because otherwise it would be possible to improve it and, together with the 
removed line, would result in even better configuration, contradicting its optimality. To solve each 
subproblem just once, it is then necessary to find out and later re-use which of the lines ending 
with some word contributes least to the overall cost. As each of the "n" words could terminate at 
most "n" potential lines, the algorithm runs in O(n ^ 2).
"""

"""
Noemi's notes: Because this only ever looks at potential breaks one line at a time, I'm not sure 
it produces optimal output in all cases.  I suspect there are some pathological inputs for which 
selecting the best lines first for the end of the text results in forcing disproportionately short 
lines earlier in the text.  I might later investigate this by trying to craft some problem inputs -- 
or maybe not because it's not a particularly efficient algo anyway.  If you can come up with any, 
let me know and I'll run them through the test suite and note them in the codebase somewhere.

I'm also confused about why we build off the min penalty for the line start instead of the line end.
I might end up checking that against various inputs to see if there's a bug.
"""

import math


def break_lines(text, max_length):
    words = text.split()
    word_count = len(words)

    # This is the var in which we track the cost of each potential line, I think
    # The matrix is word_count lists of word_count weights, pre-populated with all zeroes
    slack_space_matrix = [[0] * word_count for _ in range(word_count)]

    # Loop through the words, and populate the matrix with the length of the empty space for each potential line beginning with that word
    for line_start in range(word_count):
        # When iterated over, this line populates the diagonal with the empty space for a line containing only the word at that index
        slack_space_matrix[line_start][line_start] = max_length - len(words[line_start])

        # And for every remaining word after the one at start_index, we can calculate the empty space
        # on a potential line beginning with the  word at start_index and ending with the one at end_index
        # by subtracting the length of the word at end_index to the length of the potential line ending one word earlier
        # Note that this value will be negative for any potential line that's longer than the max length
        #
        # (Is this really more efficient than calculating the length of the entire potential line at once?
        # Probably depends on language / interpreter version.)
        for line_end in range(line_start + 1, word_count):
            slack_space_matrix[line_start][line_end] = (
                slack_space_matrix[line_start][line_end - 1] - len(words[line_end]) - 1
            )

    # Using "penalties" again based on the squares of how much shorter each line is than the max
    # but here we're storing a list of them, one for each word
    # first one is set to zero and the rest are set to a prohibitively high value
    # The value at each index represents the lowest penalty we've found so far for any line ENDING at that word
    # Each word's min penalty is the value at index (word_index + 1)
    min_penalties = [0] + [10**20] * word_count
    # For each word at index i, the value at i in this list will store the optimal starting word index for a line ENDING at word i
    optimal_start_for_end = [0] * word_count

    # Loop through our potential lines.  The way the loop works is that:
    # We start with a line of just the first word in the text
    # The inner loop moves the line start backwards until it hits the first word in the text,
    # Then the outer loop moves the line end forwards and resets the line start to match the line end
    # (for a line of just the word after the last potential line end)
    for line_end in range(word_count):
        line_start = line_end

        while line_start >= 0:
            # If it's is longer than the max length, we want a prohibitive penalty for this potential line
            # I don't know why we're not using an even more massive penalty or otherwise completely disqualifying this line
            # Tho I suppose 10^10 should be truly prohibitive for for any max length < 100K
            if slack_space_matrix[line_start][line_end] < 0:
                line_penalty = 10**10

            # for a valid potential line
            else:
                # this line's penalty is the penalty for the best option so far for the line start
                # (the longest line so far starting there) plus the square of the extra space for the line
                # We'll have already populated that value because the line start was the line end for a
                # previous iteration (unless this is the first iteration, and the penalty for the first
                # word was populated to 0)
                #
                # Noemi says: I'm still not sure this penalty corresponds to anything
                # specific to the line start, tho, rather than the line end?
                line_penalty = (
                    min_penalties[line_start]
                    + slack_space_matrix[line_start][line_end] ** 2
                )

            # Unless the line is too long, it's the best option we've found so far for a line that would end at the current ending index
            # So save this starting word as a potential break point for this ending word
            if line_penalty < min_penalties[line_end + 1]:
                min_penalties[line_end + 1] = line_penalty
                optimal_start_for_end[line_end] = line_start

            line_start -= 1

    lines = []
    line_end = word_count

    # We assemble our lines by working backwards from the last word of the text
    while line_end > 0:
        # We find the best starting point for the line ending with the current word
        line_start = optimal_start_for_end[line_end - 1]
        # Make that line
        lines.append(" ".join(words[line_start:line_end]))
        # Then move to look at what the previous line would be
        line_end = line_start

    lines.reverse()
    return lines


# skip tests with inputs more than this number of words long
break_lines.max_test_length = math.inf
