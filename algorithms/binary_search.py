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

The method using dynamic programming can be written as two nested loops: 
the outer one iterates over every word and the inner one searches for the most 
suitable break. Hirschberg and Larmore showed in 1987 an algorithm which is 
able to use binary search instead of the inner loop in the case the weight 
function is "concave". It turns out that the penalty discussed thus far can be 
made to satisfy this property by handling the "infinities" slightly differently, 
giving an overall time of O(n * log n). A similar algorithm due to Galil and 
Giancarlo from 1989[1] is given below.

The concave property says: w(i, j) + w(i', j') <= w(i', j) + w(i, j'), where i < i' < j < j'.

[1] Z. Galil, R. Giancarlo. Speeding up dynamic programming with applications 
to molecular biology. Theoretical Computer Science 64, 1989.
"""


from collections import deque


def break_lines(text, max_length):
    words = text.split()
    count = len(words)
    offsets = [0]
    for w in words:
        offsets.append(offsets[-1] + len(w))

    minima = [0] * (count + 1)
    breaks = [0] * (count + 1)

    def c(i, j):
        w = offsets[j] - offsets[i] + j - i - 1
        if w > max_length:
            return 10**10 * (w - max_length)
        return minima[i] + (max_length - w) ** 2

    def h(l, k):
        low, high = l + 1, count
        while low < high:
            mid = (low + high) // 2
            if c(l, mid) <= c(k, mid):
                high = mid
            else:
                low = mid + 1
        if c(l, high) <= c(k, high):
            return high
        return l + 2

    q = deque([(0, 1)])
    for j in range(1, count + 1):
        l = q[0][0]
        if c(j - 1, j) <= c(l, j):
            minima[j] = c(j - 1, j)
            breaks[j] = j - 1
            q.clear()
            q.append((j - 1, j + 1))
        else:
            minima[j] = c(l, j)
            breaks[j] = l
            while c(j - 1, q[-1][1]) <= c(q[-1][0], q[-1][1]):
                q.pop()
            q.append((j - 1, h(j - 1, q[-1][0])))
            if j + 1 == q[1][1]:
                q.popleft()
            else:
                q[0] = q[0][0], (q[0][1] + 1)

    lines = []
    j = count
    while j > 0:
        i = breaks[j]
        lines.append(" ".join(words[i:j]))
        j = i
    lines.reverse()
    return lines
