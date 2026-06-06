from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare students and plays
students = ["Jiang", "Kramer", "Lopez", "Megregian", "O_Neill"]
plays = ["Sunset", "Tamerlane", "Undulation"]

# Create a dictionary to map each student to a set of plays they review
# We represent each student's reviews as a list of Booleans indicating if they review each play
student_reviews = {s: [Bool(f"{s}_reviews_{p}") for p in plays] for s in students}

# Helper function to get the number of plays a student reviews
def num_plays_reviewed(s):
    return Sum([If(student_reviews[s][i], 1, 0) for i in range(len(plays))])

# Helper function to get the set of plays a student reviews as a list of Booleans
def reviews_set(s):
    return student_reviews[s]

# Base constraints
solver = Solver()

# Each student reviews one or more of exactly three plays (no more, no less)
for s in students:
    # At least one play
    solver.add(Or(student_reviews[s]))
    # Exactly three plays (but there are only three plays, so this is redundant)
    # We assume they can review any subset of the three plays, but at least one

# Kramer and Lopez each review fewer of the plays than Megregian
solver.add(num_plays_reviewed("Kramer") < num_plays_reviewed("Megregian"))
solver.add(num_plays_reviewed("Lopez") < num_plays_reviewed("Megregian"))

# Neither Lopez nor Megregian reviews any play Jiang reviews
for p in plays:
    # If Jiang reviews p, then Lopez and Megregian do not review p
    solver.add(Implies(student_reviews["Jiang"][plays.index(p)], 
                       Not(student_reviews["Lopez"][plays.index(p)])))
    solver.add(Implies(student_reviews["Jiang"][plays.index(p)], 
                       Not(student_reviews["Megregian"][plays.index(p)])))

# Kramer and O'Neill both review Tamerlane
solver.add(student_reviews["Kramer"][plays.index("Tamerlane")])
solver.add(student_reviews["O_Neill"][plays.index("Tamerlane")])

# Exactly two of the students review exactly the same play or plays as each other
# We need to find a pair of students with identical review sets
# We will enforce this by ensuring there is exactly one pair with identical sets
# To do this, we can iterate over all pairs and ensure exactly one pair is equal

# Generate all possible pairs of students
pairs = [(students[i], students[j]) for i in range(len(students)) for j in range(i+1, len(students))]

# For each pair, we can check if their review sets are equal
# We will use a list to track which pairs are equal
pair_equal = [Bool(f"pair_{i}_{j}_equal") for (i, j) in pairs]

# For each pair, if their review sets are equal, then pair_equal is True
for idx, (s1, s2) in enumerate(pairs):
    # The review sets are equal if for all plays, both review or both do not review
    equal_constraints = And([
        student_reviews[s1][p] == student_reviews[s2][p] for p in range(len(plays))
    ])
    solver.add(Implies(pair_equal[idx], equal_constraints))
    solver.add(Implies(equal_constraints, pair_equal[idx]))

# Exactly two students have the same review set
solver.add(Sum(pair_equal) == 1)

# Additional constraint: Exactly three of the students review Undulation
solver.add(Sum([If(student_reviews[s][plays.index("Undulation")], 1, 0) for s in students]) == 3)

# Now, evaluate the multiple choice options
found_options = []

# Option A: Megregian does not review Undulation
solver.push()
solver.add(Not(student_reviews["Megregian"][plays.index("Undulation")]))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: O'Neill does not review Undulation
solver.push()
solver.add(Not(student_reviews["O_Neill"][plays.index("Undulation")]))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Jiang reviews Undulation
solver.push()
solver.add(student_reviews["Jiang"][plays.index("Undulation")])
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Lopez reviews Tamerlane
solver.push()
solver.add(student_reviews["Lopez"][plays.index("Tamerlane")])
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: O'Neill reviews Sunset
solver.push()
solver.add(student_reviews["O_Neill"][plays.index("Sunset")])
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")