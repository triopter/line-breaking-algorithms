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
# algorithms/brute_force.py
# Start of Selection

def break_lines(text, max_width):
    words = text.split()
    total_words = len(words)

    minimum_penalty = 10 ** 20
    optimal_breaks = ()
    for breaks in get_all_combinations(range(1, total_words)):
        current_penalty = 0
        current_index = 0
        for next_break_index in chain(breaks, (total_words,)):
            line_width = len(' '.join(words[current_index:next_break_index]))
            if line_width > max_width:
                break
            current_penalty += (max_width - line_width) ** 2
            current_index = next_break_index
        else:
            if current_penalty < minimum_penalty:
                minimum_penalty = current_penalty
                optimal_breaks = breaks

    formatted_lines = []
    current_index = 0
    for next_break_index in chain(optimal_breaks, (total_words,)):
        formatted_lines.append(' '.join(words[current_index:next_break_index]))
        current_index = next_break_index
    return formatted_lines
