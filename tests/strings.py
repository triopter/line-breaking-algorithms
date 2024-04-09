import random
from algorithms.shortest_path import break_lines as break_default
from collections import namedtuple

# Each tuple is an input string, a max char length to break to, and an expected output

InputLengthOutput = namedtuple(
    "InputLengthOutput", ("name", "input", "max_line_length", "output")
)

INPUTS_LENGTHS_OUTPUTS = [
    InputLengthOutput(
        "original test case",
        "a b c d e f g h i j k l m n o p qqqqqqqqq",
        9,
        """\
a b c d
e f g h
i j k l
m n o p
qqqqqqqqq\
""",
    ),
    InputLengthOutput(
        # Will fail in case of regressions in the binary_search algorithm
        "Gilbert and Sullivan",
        "To sit in solemn silence on a dull, dark dock",
        16,
        """\
To sit in solemn
silence on a
dull, dark dock\
""",
    ),
    #     InputLengthOutput(
    #         "failure smoke",
    #         "a b c d e f g h i j k l m n o p qqqqqqqqq",
    #         15,
    #         """\
    # a b c d
    # e f g h
    # i j k l
    # m n o p
    # qqqqqqqqq\
    #     """,
    #     ),
]

NUM_KNOWN_TESTS = len(INPUTS_LENGTHS_OUTPUTS)

LINE_LENGTH_RANGE = [10, 100]
TEXT_LENGTH_RANGE = [1, 100]
NUM_RANDOM_TESTS = 20


def rand_word(max_length):
    return "a" * random.randint(1, max_length)


for i in range(NUM_RANDOM_TESTS):
    # for now assuming that shortest_path is correct
    line_len = random.randint(*LINE_LENGTH_RANGE)
    text_len = random.randint(*TEXT_LENGTH_RANGE)
    text = " ".join([rand_word(line_len) for i in range(text_len)])

    INPUTS_LENGTHS_OUTPUTS.append(
        InputLengthOutput(
            f"random {NUM_KNOWN_TESTS + i}",
            text,
            line_len,
            "\n".join(break_default(text, line_len)),
        )
    )

from pprint import pprint

pprint([(i, test) for i, test in enumerate(INPUTS_LENGTHS_OUTPUTS)])
