from z3 import *

# Declare the plays as constants
Sunset, Tamerlane, Undulation = Ints('Sunset Tamerlane Undulation')
# Assign unique integer values to each play for set operations
play_encoding = {Sunset: 0, Tamerlane: 1, Undulation: 2}

# Declare students
Jiang, Kramer, Lopez, Megregian, ONeill = Ints('Jiang Kramer Lopez Megregian ONeill')

# Each student's reviews are represented as a set of plays they review
# We will use BitVecs to represent sets of plays (each play is a bit)
# Since there are 3 plays, we can use a 3-bit BitVec for each student
# Bit 0: Sunset, Bit 1: Tamerlane, Bit 2: Undulation
Jiang_reviews = BitVec('Jiang_reviews', 3)
Kramer_reviews = BitVec('Kramer_reviews', 3)
Lopez_reviews = BitVec('Lopez_reviews', 3)
Megregian_reviews = BitVec('Megregian_reviews', 3)
ONeill_reviews = BitVec('ONeill_reviews', 3)

solver = Solver()

# Helper function to extract the number of plays reviewed from a BitVec
# (counts the number of set bits)
def count_plays(reviews):
    return Sum([(reviews >> i) & 1 for i in range(3)])

# Helper function to check if a student reviews a specific play
def reviews_play(student, play):
    # play is an Int, but we need to map it to a bit index
    # Since play_encoding maps plays to 0,1,2, we can use that
    bit_index = play_encoding[play]
    return (student >> bit_index) & 1 == 1

# Constraint: Each student reviews one or more plays
solver.add(count_plays(Jiang_reviews) >= 1)
solver.add(count_plays(Kramer_reviews) >= 1)
solver.add(count_plays(Lopez_reviews) >= 1)
solver.add(count_plays(Megregian_reviews) >= 1)
solver.add(count_plays(ONeill_reviews) >= 1)

# Constraint: Kramer and Lopez each review fewer plays than Megregian
solver.add(count_plays(Kramer_reviews) < count_plays(Megregian_reviews))
solver.add(count_plays(Lopez_reviews) < count_plays(Megregian_reviews))

# Constraint: Neither Lopez nor Megregian reviews any play Jiang reviews
# This means the set of plays Jiang reviews must be disjoint from Lopez and Megregian
# If Jiang reviews a play, Lopez and Megregian must not review it
for play in [Sunset, Tamerlane, Undulation]:
    # If Jiang reviews the play, Lopez and Megregian must not
    solver.add(Implies(reviews_play(Jiang_reviews, play), 
                       Not(reviews_play(Lopez_reviews, play))))
    solver.add(Implies(reviews_play(Jiang_reviews, play), 
                       Not(reviews_play(Megregian_reviews, play))))

# Constraint: Kramer and O'Neill both review Tamerlane
solver.add(reviews_play(Kramer_reviews, Tamerlane))
solver.add(reviews_play(ONeill_reviews, Tamerlane))

# Constraint: Exactly two of the students review exactly the same play or plays as each other
# We need to find exactly one pair of students with identical review sets
# We will enforce that there is exactly one pair with equal review sets
students = [Jiang_reviews, Kramer_reviews, Lopez_reviews, Megregian_reviews, ONeill_reviews]
unique_pairs = []
for i in range(len(students)):
    for j in range(i+1, len(students)):
        # Create a condition for equality of review sets
        equal_reviews = (students[i] == students[j])
        unique_pairs.append(equal_reviews)

# Exactly one pair must be equal
solver.add(Sum(unique_pairs) == 1)

# Additional condition: Jiang does not review Tamerlane
solver.add(Not(reviews_play(Jiang_reviews, Tamerlane)))

# Now, evaluate the multiple-choice options
# We will check each option to see if it must be true
found_options = []

# Option A: Jiang reviews Sunset
solver.push()
solver.add(Not(reviews_play(Jiang_reviews, Sunset)))
if solver.check() == sat:
    # If it's possible for Jiang to not review Sunset, then A is not necessarily true
    solver.pop()
else:
    # If it's unsat to assume Jiang does not review Sunset, then A must be true
    solver.pop()
    found_options.append("A")

# Option B: Lopez reviews Undulation
solver.push()
solver.add(Not(reviews_play(Lopez_reviews, Undulation)))
if solver.check() == unsat:
    # If it's unsat to assume Lopez does not review Undulation, then B must be true
    solver.pop()
    found_options.append("B")
else:
    solver.pop()

# Option C: Megregian reviews Sunset
solver.push()
solver.add(Not(reviews_play(Megregian_reviews, Sunset)))
if solver.check() == unsat:
    # If it's unsat to assume Megregian does not review Sunset, then C must be true
    solver.pop()
    found_options.append("C")
else:
    solver.pop()

# Option D: Megregian reviews Tamerlane
solver.push()
solver.add(Not(reviews_play(Megregian_reviews, Tamerlane)))
if solver.check() == unsat:
    # If it's unsat to assume Megregian does not review Tamerlane, then D must be true
    solver.pop()
    found_options.append("D")
else:
    solver.pop()

# Option E: O'Neill reviews Undulation
solver.push()
solver.add(Not(reviews_play(ONeill_reviews, Undulation)))
if solver.check() == unsat:
    # If it's unsat to assume O'Neill does not review Undulation, then E must be true
    solver.pop()
    found_options.append("E")
else:
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")