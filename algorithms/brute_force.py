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
An immediate approach is to try to search trough all the possible break configurations 
and return the best one. Since any two consecutive words might get split up by a break, 
there are order of O(2 ^ n) alternatives. Consequently, it is not feasible to form a 
paragraph of more than 30 - 40 words.
"""

from itertools import combinations, chain


def get_all_scenarios(word_count):
    """
    Input: the number of words in the text
    Returns an iterable of iterables.  Each iterable is a set of word indices
    representing one of all possible word-break scenarios.
    Each iterable contains the word indices after which we would break in that scenario.
    """
    word_indices = list(range(1, word_count))
    words_len_range = range(len(word_indices) + 1)
    return chain.from_iterable(
        combinations(word_indices, num_words) for num_words in words_len_range
    )


def break_lines(text, max_length):
    words = text.split()
    word_count = len(words)

    # Each scenario is evaluated with a "penalty" representing how good a fit it is
    # The lowest penalty wins.  Here we're starting with a theoretically very high penalty
    # with the expectation that the first scenario will immediately beat it.
    # This number does set a ceiling on the size of the text we can evaluate.
    #
    # Each scenario's total penalty is the sum of squares of how much shorter lines are than
    # the max width, so penalties are much higher for shorter lines
    #
    # @TODO: what happens if we set this to Infinity?
    min_penalty = 10**20
    # Lists the word indices after which we would break
    optimal_scenario = ()

    for scenario in get_all_scenarios(word_count):
        # We sum up the penalty for the scenario starting from zero
        scenario_penalty = 0
        # starting with the zeroth word
        line_start_word_num = 0

        # calculate the line length for each line in the scenario
        for break_after_word_num in chain(scenario, (word_count,)):
            # mock up the line by joining all the words in it, and check its length
            line_width = len(" ".join(words[line_start_word_num:break_after_word_num]))

            if line_width > max_length:
                # this scenario is invalid because at least one of its lines is too long
                # skip to the next scenario
                break

            # calculate this line's penalty and add it to the scenario's
            scenario_penalty += (max_length - line_width) ** 2

            # set the starting point for the next line
            line_start_word_num = break_after_word_num

        else:
            # We hit this clause only if all our lines were within our max length
            # Check if this is the best scenario so far, and if so, save it as our optimal scenario so far
            if scenario_penalty < min_penalty:
                min_penalty = scenario_penalty
                optimal_scenario = scenario

    formatted_lines = []
    line_start_word_num = 0

    # assemble all the lines for the scenario
    for break_after_word_num in chain(optimal_scenario, (word_count,)):
        formatted_lines.append(
            " ".join(words[line_start_word_num:break_after_word_num])
        )
        line_start_word_num = break_after_word_num

    return formatted_lines
