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

# Create the solver
solver = Solver()

# Constraint 1: Each student reviews one or more of exactly three plays (no more, no less)
for s in students:
    # Each student reviews at least one play
    solver.add(Or(student_reviews[s]), f"Each student must review at least one play: {s}")

# Constraint 2: Kramer and Lopez each review fewer of the plays than Megregian
solver.add(num_plays_reviewed("Kramer") < num_plays_reviewed("Megregian"), "Kramer reviews fewer plays than Megregian")
solver.add(num_plays_reviewed("Lopez") < num_plays_reviewed("Megregian"), "Lopez reviews fewer plays than Megregian")

# Constraint 3: Neither Lopez nor Megregian reviews any play Jiang reviews
for p in plays:
    # If Jiang reviews a play, Lopez and Megregian do not
    solver.add(Implies(student_reviews["Jiang"][plays.index(p)], 
                       Not(student_reviews["Lopez"][plays.index(p)])))
    solver.add(Implies(student_reviews["Jiang"][plays.index(p)], 
                       Not(student_reviews["Megregian"][plays.index(p)])))

# Constraint 4: Kramer and O'Neill both review Tamerlane
solver.add(student_reviews["Kramer"][plays.index("Tamerlane")], "Kramer reviews Tamerlane")
solver.add(student_reviews["O_Neill"][plays.index("Tamerlane")], "O'Neill reviews Tamerlane")

# Constraint 5: Exactly two of the students review exactly the same play or plays as each other
# We need to find exactly one pair of students with identical review sets
# We will enforce that there is exactly one pair with identical review sets
# To do this, we will:
# 1. Ensure that at least one pair of students has identical review sets
# 2. Ensure that no more than one pair of students has identical review sets

# List all possible pairs of students
student_pairs = [(students[i], students[j]) for i in range(len(students)) for j in range(i+1, len(students))]

# We will collect the pairs that have identical review sets
identical_pairs = []
for s1, s2 in student_pairs:
    # Check if the two students have identical review sets
    identical = And([student_reviews[s1][i] == student_reviews[s2][i] for i in range(len(plays))])
    identical_pairs.append(identical)

# There must be exactly one pair with identical review sets
solver.add(Or(identical_pairs), "At least one pair of students must have identical review sets")
solver.add(AtMost(*identical_pairs, 1), "At most one pair of students can have identical review sets")

# Now, evaluate the multiple choice options
# We will check each option to see if it is consistent with the constraints
found_options = []

# Option A: Jiang, Kramer
opt_a_constr = And(
    student_reviews["Jiang"][plays.index("Tamerlane")] == False,
    student_reviews["Kramer"][plays.index("Tamerlane")] == True,
    student_reviews["O_Neill"][plays.index("Tamerlane")] == False
)

# Option B: Kramer, O'Neill
opt_b_constr = And(
    student_reviews["Kramer"][plays.index("Tamerlane")] == True,
    student_reviews["O_Neill"][plays.index("Tamerlane")] == True,
    student_reviews["Jiang"][plays.index("Tamerlane")] == False
)

# Option C: Kramer, Lopez, O'Neill
opt_c_constr = And(
    student_reviews["Kramer"][plays.index("Tamerlane")] == True,
    student_reviews["Lopez"][plays.index("Tamerlane")] == True,
    student_reviews["O_Neill"][plays.index("Tamerlane")] == True,
    student_reviews["Jiang"][plays.index("Tamerlane")] == False
)

# Option D: Kramer, Megregian, O'Neill
opt_d_constr = And(
    student_reviews["Kramer"][plays.index("Tamerlane")] == True,
    student_reviews["Megregian"][plays.index("Tamerlane")] == True,
    student_reviews["O_Neill"][plays.index("Tamerlane")] == True,
    student_reviews["Jiang"][plays.index("Tamerlane")] == False
)

# Option E: Lopez, Megregian, O'Neill
opt_e_constr = And(
    student_reviews["Lopez"][plays.index("Tamerlane")] == True,
    student_reviews["Megregian"][plays.index("Tamerlane")] == True,
    student_reviews["O_Neill"][plays.index("Tamerlane")] == True,
    student_reviews["Jiang"][plays.index("Tamerlane")] == False
)

# Test each option
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