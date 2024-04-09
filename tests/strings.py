from collections import namedtuple

# Each tuple is an input string, a max char length to break to, and an expected output

InputLengthOutput = namedtuple(
    "InputLengthOutput", ("name", "input", "max_line_length", "output")
)

INPUTS_LENGTHS_OUTPUTS = (
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
)
