from z3 import *

# BENCHMARK_MODE: ON (model-finding with refinement on unsat)
BENCHMARK_MODE = True

# Declare students and plays
students = ["Jiang", "Kramer", "Lopez", "Megregian", "O_Neill"]
plays = ["Sunset", "Tamerlane", "Undulation"]

# Create a solver
solver = Solver()

# Declare review variables: reviews[s][p] is True if student s reviews play p
reviews = {s: {p: Bool(f"reviews_{s}_{p}") for p in plays} for s in students}

# Helper: count the number of plays each student reviews
def count_plays(s):
    return Sum([If(reviews[s][p], 1, 0) for p in plays])

# Constraint 1: Each student reviews one or more plays
for s in students:
    solver.add(Or([reviews[s][p] for p in plays]))

# Constraint 2: Kramer and Lopez each review fewer plays than Megregian
solver.add(count_plays("Kramer") < count_plays("Megregian"))
solver.add(count_plays("Lopez") < count_plays("Megregian"))

# Constraint 3: Neither Lopez nor Megregian reviews any play Jiang reviews
for p in plays:
    solver.add(Not(And(reviews["Jiang"][p], reviews["Lopez"][p])))
    solver.add(Not(And(reviews["Jiang"][p], reviews["Megregian"][p])))

# Constraint 4: Kramer and O'Neill both review Tamerlane
solver.add(reviews["Kramer"]["Tamerlane"])
solver.add(reviews["O_Neill"]["Tamerlane"])

# Constraint 5: Exactly two of the students review exactly the same play or plays as each other
# We need to find exactly one pair of students with identical review sets
# Generate all pairs of students
student_pairs = [(s1, s2) for i, s1 in enumerate(students) for s2 in students[i+1:]]

# For each pair, we can say they are equal or not
pair_equal = {pair: Bool(f"pair_equal_{pair[0]}_{pair[1]}") for pair in student_pairs}

# For each pair, if they are equal, all their review variables must match
for (s1, s2), eq in pair_equal.items():
    for p in plays:
        solver.add(Implies(eq, reviews[s1][p] == reviews[s2][p]))
        solver.add(Implies(Not(eq), reviews[s1][p] != reviews[s2][p]))

# Exactly one pair must be equal
solver.add(Sum([If(eq, 1, 0) for eq in pair_equal.values()]) == 1)

# Constraint 6: Exactly three of the students review Undulation
solver.add(Sum([If(reviews[s]["Undulation"], 1, 0) for s in students]) == 3)

# Check base constraints
result = solver.check()

if result == sat:
    print("STATUS: sat")
    model = solver.model()
    # Print some debug info
    for s in students:
        plays_reviewed = [p for p in plays if is_true(model[reviews[s][p]])]
        print(f"{s} reviews: {plays_reviewed}")
else:
    print("STATUS: unknown")
    print("Base constraints could not be satisfied")
    exit(0)

# Now evaluate each multiple-choice option
found_options = []

# Option A: Megregian does not review Undulation
solver.push()
solver.add(Not(reviews["Megregian"]["Undulation"]))
opt_a_res = solver.check()
solver.pop()
if opt_a_res == sat:
    found_options.append("A")

# Option B: O'Neill does not review Undulation
solver.push()
solver.add(Not(reviews["O_Neill"]["Undulation"]))
opt_b_res = solver.check()
solver.pop()
if opt_b_res == sat:
    found_options.append("B")

# Option C: Jiang reviews Undulation
solver.push()
solver.add(reviews["Jiang"]["Undulation"])
opt_c_res = solver.check()
solver.pop()
if opt_c_res == sat:
    found_options.append("C")

# Option D: Lopez reviews Tamerlane
solver.push()
solver.add(reviews["Lopez"]["Tamerlane"])
opt_d_res = solver.check()
solver.pop()
if opt_d_res == sat:
    found_options.append("D")

# Option E: O'Neill reviews Sunset
solver.push()
solver.add(reviews["O_Neill"]["Sunset"])
opt_e_res = solver.check()
solver.pop()
if opt_e_res == sat:
    found_options.append("E")

# Determine the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")