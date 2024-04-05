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


def break_lines(text, max_length):
    words = text.split()
    count = len(words)
    slack = [[0] * count for i in range(count)]
    for i in range(count):
        slack[i][i] = max_length - len(words[i])
        for j in range(i + 1, count):
            slack[i][j] = slack[i][j - 1] - len(words[j]) - 1

    minima = [0] + [10**20] * count
    breaks = [0] * count
    for j in range(count):
        i = j
        while i >= 0:
            if slack[i][j] < 0:
                cost = 10**10
            else:
                cost = minima[i] + slack[i][j] ** 2
            if minima[j + 1] > cost:
                minima[j + 1] = cost
                breaks[j] = i
            i -= 1

    lines = []
    j = count
    while j > 0:
        i = breaks[j - 1]
        lines.append(" ".join(words[i:j]))
        j = i
    lines.reverse()
    return lines
