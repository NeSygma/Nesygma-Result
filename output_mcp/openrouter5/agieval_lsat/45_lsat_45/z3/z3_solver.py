from z3 import *

# Students: Jiang, Kramer, Lopez, Megregian, O'Neill
# Plays: Sunset (S), Tamerlane (T), Undulation (U)
# Each student reviews one or more of exactly three plays.
# So each student reviews a non-empty subset of {S, T, U}.

students = ["Jiang", "Kramer", "Lopez", "Megregian", "ONeill"]
plays = ["Sunset", "Tamerlane", "Undulation"]

# We'll use Boolean variables: student_reviews[student][play]
# True means the student reviews that play.
reviews = {s: {p: Bool(f"{s}_{p}") for p in plays} for s in students}

solver = Solver()

# 1. Each student reviews at least one play (one or more of exactly three plays)
for s in students:
    solver.add(Or([reviews[s][p] for p in plays]))

# 2. Kramer and Lopez each review fewer of the plays than Megregian.
# Count number of plays reviewed by each.
# Use Sum of If.
for s in ["Kramer", "Lopez"]:
    solver.add(
        Sum([If(reviews[s][p], 1, 0) for p in plays]) <
        Sum([If(reviews["Megregian"][p], 1, 0) for p in plays])
    )

# 3. Neither Lopez nor Megregian reviews any play Jiang reviews.
# For each play, if Jiang reviews it, then Lopez does not and Megregian does not.
for p in plays:
    solver.add(Implies(reviews["Jiang"][p], Not(reviews["Lopez"][p])))
    solver.add(Implies(reviews["Jiang"][p], Not(reviews["Megregian"][p])))

# 4. Kramer and O'Neill both review Tamerlane.
solver.add(reviews["Kramer"]["Tamerlane"] == True)
solver.add(reviews["ONeill"]["Tamerlane"] == True)

# 5. Exactly two of the students review exactly the same play or plays as each other.
# This means there is exactly one pair of students who have identical review sets,
# and no other pair does.

# First, define a helper: for two students s1, s2, they have the same review set
# iff for every play p, reviews[s1][p] == reviews[s2][p].
def same_set(s1, s2):
    return And([reviews[s1][p] == reviews[s2][p] for p in plays])

# Count the number of pairs (i, j) with i < j that have identical sets.
pair_vars = []
pair_list = []
for i in range(len(students)):
    for j in range(i+1, len(students)):
        b = Bool(f"pair_{students[i]}_{students[j]}")
        pair_vars.append(b)
        pair_list.append((students[i], students[j]))
        solver.add(b == same_set(students[i], students[j]))

# Exactly two students share the same set => exactly one pair is True.
solver.add(Sum([If(b, 1, 0) for b in pair_vars]) == 1)

# Additional condition from the question: Exactly three of the students review Undulation.
solver.add(Sum([If(reviews[s]["Undulation"], 1, 0) for s in students]) == 3)

# Now evaluate each option
# (A) Megregian does not review Undulation.
opt_a = Not(reviews["Megregian"]["Undulation"])

# (B) O'Neill does not review Undulation.
opt_b = Not(reviews["ONeill"]["Undulation"])

# (C) Jiang reviews Undulation.
opt_c = reviews["Jiang"]["Undulation"]

# (D) Lopez reviews Tamerlane.
opt_d = reviews["Lopez"]["Tamerlane"]

# (E) O'Neill reviews Sunset.
opt_e = reviews["ONeill"]["Sunset"]

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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