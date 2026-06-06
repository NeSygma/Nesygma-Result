from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Create a solver
solver = Solver()

# Define the plays as bit positions
Sunset = 0
Tamerlane = 1
Undulation = 2

# Define the students
students = ["Jiang", "Kramer", "Lopez", "Megregian", "O'Neill"]

# Create a dictionary to hold the review bitmask for each student as BitVec
reviews = {s: BitVec(f"reviews_{s}", 3) for s in students}

# Helper function to count the number of plays reviewed (number of bits set)
def count_plays(review_mask):
    return Sum([If(Extract(i, i, review_mask) == 1, 1, 0) for i in range(3)])

# Add constraints for each student reviewing at least one play
for s in students:
    solver.add(count_plays(reviews[s]) >= 1)  # At least one play reviewed
    solver.add(count_plays(reviews[s]) <= 3)  # At most three plays

# Constraint: Kramer and Lopez each review fewer plays than Megregian
solver.add(count_plays(reviews["Kramer"]) < count_plays(reviews["Megregian"]))
solver.add(count_plays(reviews["Lopez"]) < count_plays(reviews["Megregian"]))

# Constraint: Neither Lopez nor Megregian reviews any play Jiang reviews
# This means the bitwise AND between Jiang's reviews and Lopez's reviews is 0
# Similarly for Megregian
solver.add(reviews["Jiang"] & reviews["Lopez"] == 0)
solver.add(reviews["Jiang"] & reviews["Megregian"] == 0)

# Constraint: Kramer and O'Neill both review Tamerlane
# Tamerlane is bit 1, so the bit must be set
solver.add(Extract(Tamerlane, Tamerlane, reviews["Kramer"]) == 1)
solver.add(Extract(Tamerlane, Tamerlane, reviews["O'Neill"]) == 1)

# Constraint: Exactly two of the students review exactly the same play or plays as each other
# This means there is exactly one pair of students with equal review sets
# All other pairs must be unequal

# Generate all possible pairs of students
pairs = [(students[i], students[j]) for i in range(len(students)) for j in range(i+1, len(students))]

# For each pair, we can check if their reviews are equal
pair_equalities = []
for (s1, s2) in pairs:
    pair_equalities.append(reviews[s1] == reviews[s2])

# We need exactly one pair to be equal
solver.add(Sum(pair_equalities) == 1)

# Now, evaluate the multiple-choice options for who reviews Tamerlane
# We need to check which option is consistent with all constraints

def reviews_tamerlane(s):
    return Extract(Tamerlane, Tamerlane, reviews[s]) == 1

# Define constraints for each option
# Option A: Jiang, Kramer
opt_a_constr = And(
    reviews_tamerlane("Jiang"),
    reviews_tamerlane("Kramer"),
    Not(reviews_tamerlane("Lopez")),
    Not(reviews_tamerlane("Megregian")),
    Not(reviews_tamerlane("O'Neill"))
)

# Option B: Kramer, O'Neill
opt_b_constr = And(
    Not(reviews_tamerlane("Jiang")),
    reviews_tamerlane("Kramer"),
    Not(reviews_tamerlane("Lopez")),
    Not(reviews_tamerlane("Megregian")),
    reviews_tamerlane("O'Neill")
)

# Option C: Kramer, Lopez, O'Neill
opt_c_constr = And(
    Not(reviews_tamerlane("Jiang")),
    reviews_tamerlane("Kramer"),
    reviews_tamerlane("Lopez"),
    Not(reviews_tamerlane("Megregian")),
    reviews_tamerlane("O'Neill")
)

# Option D: Kramer, Megregian, O'Neill
opt_d_constr = And(
    Not(reviews_tamerlane("Jiang")),
    reviews_tamerlane("Kramer"),
    Not(reviews_tamerlane("Lopez")),
    reviews_tamerlane("Megregian"),
    reviews_tamerlane("O'Neill")
)

# Option E: Lopez, Megregian, O'Neill
opt_e_constr = And(
    Not(reviews_tamerlane("Jiang")),
    Not(reviews_tamerlane("Kramer")),
    reviews_tamerlane("Lopez"),
    reviews_tamerlane("Megregian"),
    reviews_tamerlane("O'Neill")
)

# Test each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
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