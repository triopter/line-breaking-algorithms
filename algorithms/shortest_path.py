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

The previous way can be sped up even further: the length offsets used to 
calculate any line length in constant time can easily be pre-processed in O(n),
rather than O(n ^ 2), and there is no point in putting ever more words on a 
line once it reaches the allowed width. The performance then improves down to 
O(n * width).

This is exactly the same result as if the text was thought of as a 
(topologically sorted) directed acyclic graph, with the nodes and arcs
 representing words and breaks, respectively. By substituting the penalties for
 the weights, the problem becomes the one of finding the shortest path which is 
 known to be solvable in linear time. Note that the number of edges remains 
 O(n * width).
 """


def break_lines(text, max_length):
    words = text.split()
    word_count = len(words)
    offsets = [0]
    for word in words:
        offsets.append(offsets[-1] + len(word))

    minima = [0] + [10**20] * word_count
    breaks = [0] * (word_count + 1)
    for current_index in range(word_count):
        next_index = current_index + 1
        while next_index <= word_count:
            current_width = (
                offsets[next_index]
                - offsets[current_index]
                + next_index
                - current_index
                - 1
            )
            if current_width > max_length:
                break
            cost = minima[current_index] + (max_length - current_width) ** 2
            if cost < minima[next_index]:
                minima[next_index] = cost
                breaks[next_index] = current_index
            next_index += 1

    lines = []
    current_position = word_count
    while current_position > 0:
        start_position = breaks[current_position]
        lines.append(" ".join(words[start_position:current_position]))
        current_position = start_position
    lines.reverse()
    return lines
