import random
from algorithms.shortest_path import break_lines as break_default
from collections import namedtuple

# Each tuple is an input string, a max char length to break to, and an expected output

InputLengthOutput = namedtuple(
    "InputLengthOutput", ("name", "input", "max_line_length", "output")
)


INPUTS_LENGTHS_OUTPUTS = []

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
            f"random {i}",
            text,
            line_len,
            "\n".join(break_default(text, line_len)),
        )
    )


ALPHA = InputLengthOutput(
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
)
GILBERT_SHORT = InputLengthOutput(
    # NOTE: Will fail in case of regressions in the binary_search algorithm
    "Gilbert and Sullivan - Short",
    "To sit in solemn silence in a dull, dark dock",
    16,
    """\
To sit in solemn
silence on a
dull, dark dock\
""",
)
GILBERT_FULL = InputLengthOutput(
    "Gilbert and Sullivan - Full",
    "To sit in solemn silence in a dull, dark dock, In a pestilential prison, with a lifelong lock, "
    "Awaiting the sensation of a short, sharp shock, From a cheap and chippy chopper on a big black block!",
    55,
    """\
To sit in solemn silence in a dull, dark dock,
In a pestilential prison, with a lifelong lock,
Awaiting the sensation of a short, sharp shock, From
a cheap and chippy chopper on a big black block!\
""",
)
PREAMBLE = InputLengthOutput(
    "Preamble to the US Constitution",
    "We the People of the United States, in Order to form a more perfect Union, establish Justice, "
    "insure domestic Tranquility, provide for the common defense, promote the general Welfare, and "
    "secure the Blessings of Liberty to ourselves and our Posterity, do ordain and establish this "
    "Constitution for the United States of America.",
    100,
    """\
We the People of the United States, in Order to form a more perfect Union, establish
Justice, insure domestic Tranquility, provide for the common defense, promote the
general Welfare, and secure the Blessings of Liberty to ourselves and our Posterity,
do ordain and establish this Constitution for the United States of America.\
""",
)
BLEAK_HOUSE = InputLengthOutput(
    "Bleak House by Charles Dickens",
    "London. Michaelmas term lately over, and the Lord Chancellor sitting in Lincoln’s Inn Hall. Implacable November weather. As "
    "much mud in the streets as if the waters had but newly retired from the face of the earth, and it would not be wonderful to "
    "meet a Megalosaurus, forty feet long or so, waddling like an elephantine lizard up Holborn Hill. Smoke lowering down from "
    "chimney-pots, making a soft black drizzle, with flakes of soot in it as big as full-grown snowflakes—gone into mourning, "
    "one might imagine, for the death of the sun. Dogs, undistinguishable in mire. Horses, scarcely better; splashed to their "
    "very blinkers. Foot passengers, jostling one another’s umbrellas in a general infection of ill temper, and losing their "
    "foot-hold at street-corners, where tens of thousands of other foot passengers have been slipping and sliding since the day "
    "broke (if this day ever broke), adding new deposits to the crust upon crust of mud, sticking at those points tenaciously "
    "to the pavement, and accumulating at compound interest. Gas looming through the fog in divers places in the streets, much "
    "as the sun may, from the spongey fields, be seen to loom by husbandman and ploughboy. Most of the shops lighted two hours "
    "before their time—as the gas seems to know, for it has a haggard and unwilling look. The raw afternoon is rawest, and the "
    "dense fog is densest, and the muddy streets are muddiest near that leaden-headed old obstruction, appropriate ornament "
    "for the threshold of a leaden-headed old corporation, Temple Bar. And hard by Temple Bar, in Lincoln’s Inn Hall, at the "
    "very heart of the fog, sits the Lord High Chancellor in his High Court of Chancery. Never can there come fog too thick, "
    "never can there come mud and mire too deep, to assort with the groping and floundering condition which this High Court "
    "of Chancery, most pestilent of hoary sinners, holds this day in the sight of heaven and earth. On such an afternoon, if "
    "ever, the Lord High Chancellor ought to be sitting here—as here he is—with a foggy glory round his head, softly fenced in "
    "with crimson cloth and curtains, addressed by a large advocate with great whiskers, a little voice, and an interminable "
    "brief, and outwardly directing his contemplation to the lantern in the roof, where he can see nothing but fog. On such "
    "an afternoon some score of members of the High Court of Chancery bar ought to be—as here they are—mistily engaged in "
    "one of the ten thousand stages of an endless cause, tripping one another up on slippery precedents, groping knee-deep "
    "in technicalities, running their goat-hair and horsehair warded heads against walls of words and making a pretence of "
    "equity with serious faces, as players might. On such an afternoon the various solicitors in the cause, some two or three "
    "of whom have inherited it from their fathers, who made a fortune by it, ought to be—as are they not?—ranged in a line, "
    "in a long matted well (but you might look in vain for truth at the bottom of it) between the registrar’s red table and "
    "the silk gowns, with bills, cross-bills, answers, rejoinders, injunctions, affidavits, issues, references to masters, "
    "masters’ reports, mountains of costly nonsense, piled before them. Well may the court be dim, with wasting candles here "
    "and there; well may the fog hang heavy in it, as if it would never get out; well may the stained-glass windows lose their "
    "colour and admit no light of day into the place; well may the uninitiated from the streets, who peep in through the glass "
    "panes in the door, be deterred from entrance by its owlish aspect and by the drawl, languidly echoing to the roof from "
    "the padded dais where the Lord High Chancellor looks into the lantern that has no light in it and where the attendant "
    "wigs are all stuck in a fog-bank! This is the Court of Chancery, which has its decaying houses and its blighted lands "
    "in every shire, which has its worn-out lunatic in every madhouse and its dead in every churchyard, which has its ruined "
    "suitor with his slipshod heels and threadbare dress borrowing and begging through the round of every man’s acquaintance, "
    "which gives to monied might the means abundantly of wearying out the right, which so exhausts finances, patience, "
    "courage, hope, so overthrows the brain and breaks the heart, that there is not an honourable man among its practitioners "
    'who would not give—who does not often give—the warning, "Suffer any wrong that can be done you rather than come here!"',
    100,
    """\
London. Michaelmas term lately over, and the Lord Chancellor sitting in Lincoln’s Inn Hall.
Implacable November weather. As much mud in the streets as if the waters had but newly retired
from the face of the earth, and it would not be wonderful to meet a Megalosaurus, forty feet long
or so, waddling like an elephantine lizard up Holborn Hill. Smoke lowering down from chimney-pots,
making a soft black drizzle, with flakes of soot in it as big as full-grown snowflakes—gone into
mourning, one might imagine, for the death of the sun. Dogs, undistinguishable in mire. Horses,
scarcely better; splashed to their very blinkers. Foot passengers, jostling one another’s umbrellas
in a general infection of ill temper, and losing their foot-hold at street-corners, where tens
of thousands of other foot passengers have been slipping and sliding since the day broke (if this
day ever broke), adding new deposits to the crust upon crust of mud, sticking at those points
tenaciously to the pavement, and accumulating at compound interest. Gas looming through the fog
in divers places in the streets, much as the sun may, from the spongey fields, be seen to loom by
husbandman and ploughboy. Most of the shops lighted two hours before their time—as the gas seems
to know, for it has a haggard and unwilling look. The raw afternoon is rawest, and the dense fog
is densest, and the muddy streets are muddiest near that leaden-headed old obstruction, appropriate
ornament for the threshold of a leaden-headed old corporation, Temple Bar. And hard by Temple
Bar, in Lincoln’s Inn Hall, at the very heart of the fog, sits the Lord High Chancellor in his
High Court of Chancery. Never can there come fog too thick, never can there come mud and mire too
deep, to assort with the groping and floundering condition which this High Court of Chancery, most
pestilent of hoary sinners, holds this day in the sight of heaven and earth. On such an afternoon,
if ever, the Lord High Chancellor ought to be sitting here—as here he is—with a foggy glory round
his head, softly fenced in with crimson cloth and curtains, addressed by a large advocate with
great whiskers, a little voice, and an interminable brief, and outwardly directing his contemplation
to the lantern in the roof, where he can see nothing but fog. On such an afternoon some score
of members of the High Court of Chancery bar ought to be—as here they are—mistily engaged in one
of the ten thousand stages of an endless cause, tripping one another up on slippery precedents,
groping knee-deep in technicalities, running their goat-hair and horsehair warded heads against
walls of words and making a pretence of equity with serious faces, as players might. On such an
afternoon the various solicitors in the cause, some two or three of whom have inherited it from
their fathers, who made a fortune by it, ought to be—as are they not?—ranged in a line, in a long
matted well (but you might look in vain for truth at the bottom of it) between the registrar’s red
table and the silk gowns, with bills, cross-bills, answers, rejoinders, injunctions, affidavits,
issues, references to masters, masters’ reports, mountains of costly nonsense, piled before them.
Well may the court be dim, with wasting candles here and there; well may the fog hang heavy in
it, as if it would never get out; well may the stained-glass windows lose their colour and admit
no light of day into the place; well may the uninitiated from the streets, who peep in through
the glass panes in the door, be deterred from entrance by its owlish aspect and by the drawl,
languidly echoing to the roof from the padded dais where the Lord High Chancellor looks into the
lantern that has no light in it and where the attendant wigs are all stuck in a fog-bank! This is
the Court of Chancery, which has its decaying houses and its blighted lands in every shire, which
has its worn-out lunatic in every madhouse and its dead in every churchyard, which has its ruined
suitor with his slipshod heels and threadbare dress borrowing and begging through the round of
every man’s acquaintance, which gives to monied might the means abundantly of wearying out the
right, which so exhausts finances, patience, courage, hope, so overthrows the brain and breaks
the heart, that there is not an honourable man among its practitioners who would not give—who
does not often give—the warning, "Suffer any wrong that can be done you rather than come here!"\
""",
)

INPUTS_LENGTHS_OUTPUTS = [
    ALPHA,
    GILBERT_SHORT,
    GILBERT_FULL,
    PREAMBLE,
    BLEAK_HOUSE,
    *INPUTS_LENGTHS_OUTPUTS,
]
