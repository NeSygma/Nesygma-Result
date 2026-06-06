from z3 import *

solver = Solver()

# Declare students and plays
students = ["Jiang", "Kramer", "Lopez", "Megregian", "O'Neill"]
plays = ["Sunset", "Tamerlane", "Undulation"]

# Each student reviews one or more of exactly three plays
# We model the reviews as a dictionary of sets: student -> set of plays reviewed
review = {s: [Bool(f"{s}_reviews_{p}") for p in plays] for s in students}

# Helper function to get the set of plays reviewed by a student
def reviews(s):
    return review[s]

# Each student reviews at least one play
for s in students:
    solver.add(Or(reviews(s)))

# Each student reviews exactly three plays (but only Sunset, Tamerlane, Undulation are allowed)
# Since there are only three plays, this means each student reviews all three plays?
# Wait, the problem says "each review one or more of exactly three plays: Sunset, Tamerlane, and Undulation"
# This likely means each student reviews a non-empty subset of the three plays.
# So we do not need to enforce that they review all three, just that they review at least one.
# The "exactly three plays" likely means that the only plays available are these three, and no others.
# So we do not need to enforce that they review exactly three plays, just that they review a subset of these three.

# Kramer and Lopez each review fewer of the plays than Megregian.
# This means the number of plays Megregian reviews is strictly greater than the number reviewed by Kramer and Lopez.
# We need to count the number of plays each student reviews.

# Count the number of plays each student reviews
count = {s: Sum([If(b, 1, 0) for b in reviews(s)]) for s in students}

# Kramer and Lopez each review fewer plays than Megregian
solver.add(count["Kramer"] < count["Megregian"])
solver.add(count["Lopez"] < count["Megregian"])

# Neither Lopez nor Megregian reviews any play Jiang reviews.
# This means: If Jiang reviews a play, then Lopez and Megregian do not review it.
for p in plays:
    solver.add(Implies(review["Jiang"][plays.index(p)], Not(review["Lopez"][plays.index(p)])))
    solver.add(Implies(review["Jiang"][plays.index(p)], Not(review["Megregian"][plays.index(p)])))

# Kramer and O'Neill both review Tamerlane.
for s in ["Kramer", "O'Neill"]:
    solver.add(review[s][plays.index("Tamerlane")] == True)

# Exactly two of the students review exactly the same play or plays as each other.
# This means there is exactly one pair of students who review the exact same set of plays.
# We need to find all pairs of students who have the same review set.

# Generate all pairs of students
pairs = [(s1, s2) for s1 in students for s2 in students if s1 < s2]

# For each pair, check if their review sets are equal
pair_equal = []
for s1, s2 in pairs:
    # Two students have the same review set if for every play, they both review it or both do not review it.
    equal = And([review[s1][i] == review[s2][i] for i in range(len(plays))])
    pair_equal.append(equal)

# Exactly one pair must be equal
solver.add(Sum([If(p, 1, 0) for p in pair_equal]) == 1)

# Now, evaluate the multiple choice options
# We need to find which option could be an accurate and complete list of the students who review ONLY Sunset.
# This means: The student(s) in the option review ONLY Sunset, and no other plays.
# We need to check each option to see if it is possible under the constraints.

found_options = []

# Option A: Lopez
solver.push()
solver.add(
    # Lopez reviews only Sunset
    And(
        review["Lopez"][plays.index("Sunset")] == True,
        review["Lopez"][plays.index("Tamerlane")] == False,
        review["Lopez"][plays.index("Undulation")] == False
    )
)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: O'Neill
solver.push()
solver.add(
    # O'Neill reviews only Sunset
    And(
        review["O'Neill"][plays.index("Sunset")] == True,
        review["O'Neill"][plays.index("Tamerlane")] == False,
        review["O'Neill"][plays.index("Undulation")] == False
    )
)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Jiang, Lopez
solver.push()
solver.add(
    # Jiang reviews only Sunset
    And(
        review["Jiang"][plays.index("Sunset")] == True,
        review["Jiang"][plays.index("Tamerlane")] == False,
        review["Jiang"][plays.index("Undulation")] == False
    ),
    # Lopez reviews only Sunset
    And(
        review["Lopez"][plays.index("Sunset")] == True,
        review["Lopez"][plays.index("Tamerlane")] == False,
        review["Lopez"][plays.index("Undulation")] == False
    )
)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Kramer, O'Neill
solver.push()
solver.add(
    # Kramer reviews only Sunset
    And(
        review["Kramer"][plays.index("Sunset")] == True,
        review["Kramer"][plays.index("Tamerlane")] == False,
        review["Kramer"][plays.index("Undulation")] == False
    ),
    # O'Neill reviews only Sunset
    And(
        review["O'Neill"][plays.index("Sunset")] == True,
        review["O'Neill"][plays.index("Tamerlane")] == False,
        review["O'Neill"][plays.index("Undulation")] == False
    )
)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Lopez, Megregian
solver.push()
solver.add(
    # Lopez reviews only Sunset
    And(
        review["Lopez"][plays.index("Sunset")] == True,
        review["Lopez"][plays.index("Tamerlane")] == False,
        review["Lopez"][plays.index("Undulation")] == False
    ),
    # Megregian reviews only Sunset
    And(
        review["Megregian"][plays.index("Sunset")] == True,
        review["Megregian"][plays.index("Tamerlane")] == False,
        review["Megregian"][plays.index("Undulation")] == False
    )
)
if solver.check() == sat:
    found_options.append("E")
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