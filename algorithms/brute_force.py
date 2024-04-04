"""
Via https://xxyxyz.org/line-breaking/:
An immediate approach is to try to search trough all the possible break configurations 
and return the best one. Since any two consecutive words might get split up by a break, 
there are order of O(2 ^ n) alternatives. Consequently, it is not feasible to form a 
paragraph of more than 30 - 40 words.
"""

from itertools import combinations, chain

def get_all_combinations(words_iterable):
    """
    Input: an ordered iterable containing the text split into words.
    Returns a list of all possible combinations of those words that maintain the ordering.
    """
    words = list(words_iterable)
    words_range = range(len(words)+1)
    return chain.from_iterable(combinations(words, num_words) for num_words in words_range)

def break_lines(text, max_width):
    words = text.split()
    count = len(words)

    minimum = 10 ** 20
    breaks = ()
    for b in powerset(range(1, count)):
        m = 0
        i = 0
        for j in chain(b, (count,)):
            w = len(' '.join(words[i:j]))
            if w > width:
                break
            m += (width - w) ** 2
            i = j
        else:
            if m < minimum:
                minimum = m
                breaks = b

    lines = []
    i = 0
    for j in chain(breaks, (count,)):
        lines.append(' '.join(words[i:j]))
        i = j
    return lines
