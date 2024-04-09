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
    count = len(words)
    offsets = [0]
    for w in words:
        offsets.append(offsets[-1] + len(w))

    minima = [0] + [10**20] * count
    breaks = [0] * (count + 1)

    def cost(i, j):
        w = offsets[j] - offsets[i] + j - i - 1
        if w > max_length:
            return 10**10 * (w - max_length)
        return minima[i] + (max_length - w) ** 2

    def smawk(rows, columns):
        stack = []
        i = 0
        while i < len(rows):
            if stack:
                c = columns[len(stack) - 1]
                if cost(stack[-1], c) < cost(rows[i], c):
                    if len(stack) < len(columns):
                        stack.append(rows[i])
                    i += 1
                else:
                    stack.pop()
            else:
                stack.append(rows[i])
                i += 1
        rows = stack

        if len(columns) > 1:
            smawk(rows, columns[1::2])

        i = j = 0
        while j < len(columns):
            if j + 1 < len(columns):
                end = breaks[columns[j + 1]]
            else:
                end = rows[-1]
            c = cost(rows[i], columns[j])
            if c < minima[columns[j]]:
                minima[columns[j]] = c
                breaks[columns[j]] = rows[i]
            if rows[i] < end:
                i += 1
            else:
                j += 2

    n = count + 1
    i = 0
    offset = 0
    while True:
        r = min(n, 2 ** (i + 1))
        edge = 2**i + offset
        smawk(range(0 + offset, edge), range(edge, r + offset))
        x = minima[r - 1 + offset]
        for j in range(2**i, r - 1):
            y = cost(j + offset, r - 1 + offset)
            if y <= x:
                n -= j
                i = 0
                offset += j
                break
        else:
            if r == n:
                break
            i = i + 1

    lines = []
    j = count
    while j > 0:
        i = breaks[j]
        lines.append(" ".join(words[i:j]))
        j = i
    lines.reverse()
    return lines
