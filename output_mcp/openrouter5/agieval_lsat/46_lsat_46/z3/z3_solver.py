from z3 import *

# Students: Jiang, Kramer, Lopez, Megregian, O'Neill
# Plays: Sunset (S), Tamerlane (T), Undulation (U)
# Each student reviews one or more of exactly three plays.
# So each student reviews a non-empty subset of {S, T, U}.

students = ["Jiang", "Kramer", "Lopez", "Megregian", "ONeill"]
plays = ["Sunset", "Tamerlane", "Undulation"]

# We'll use Boolean variables: student_review[student][play] = True if student reviews that play
# Index mapping
s_idx = {name: i for i, name in enumerate(students)}
p_idx = {"Sunset": 0, "Tamerlane": 1, "Undulation": 2}

review = [[Bool(f"{s}_{p}") for p in plays] for s in students]

solver = Solver()

# 1. Each student reviews one or more plays (non-empty subset)
for i in range(len(students)):
    solver.add(Or([review[i][j] for j in range(3)]))

# 2. Kramer and Lopez each review fewer of the plays than Megregian.
# Count plays reviewed by each student
kramer_count = Sum([If(review[s_idx["Kramer"]][j], 1, 0) for j in range(3)])
lopez_count = Sum([If(review[s_idx["Lopez"]][j], 1, 0) for j in range(3)])
megregian_count = Sum([If(review[s_idx["Megregian"]][j], 1, 0) for j in range(3)])

solver.add(kramer_count < megregian_count)
solver.add(lopez_count < megregian_count)

# 3. Neither Lopez nor Megregian reviews any play Jiang reviews.
# For each play, if Jiang reviews it, then Lopez does NOT review it, and Megregian does NOT review it.
for j in range(3):
    solver.add(Implies(review[s_idx["Jiang"]][j], Not(review[s_idx["Lopez"]][j])))
    solver.add(Implies(review[s_idx["Jiang"]][j], Not(review[s_idx["Megregian"]][j])))

# 4. Kramer and O'Neill both review Tamerlane.
solver.add(review[s_idx["Kramer"]][p_idx["Tamerlane"]])
solver.add(review[s_idx["ONeill"]][p_idx["Tamerlane"]])

# 5. Exactly two of the students review exactly the same play or plays as each other.
# This means there is exactly one pair of students who have identical review sets.
# We'll define for each pair (i, j) whether they have identical review sets.
pair_vars = []
for i in range(len(students)):
    for j in range(i+1, len(students)):
        # identical if for all plays, review[i][k] == review[j][k]
        identical = Bool(f"identical_{students[i]}_{students[j]}")
        solver.add(identical == And([review[i][k] == review[j][k] for k in range(3)]))
        pair_vars.append(identical)

# Exactly one pair is identical
solver.add(Sum([If(v, 1, 0) for v in pair_vars]) == 1)

# Now evaluate each option.
# Each option lists the students who review Tamerlane.
# We need to check if that list is an accurate and complete list of students reviewing Tamerlane.

# Option A: Jiang, Kramer
opt_a = And(
    review[s_idx["Jiang"]][p_idx["Tamerlane"]],
    review[s_idx["Kramer"]][p_idx["Tamerlane"]],
    Not(review[s_idx["Lopez"]][p_idx["Tamerlane"]]),
    Not(review[s_idx["Megregian"]][p_idx["Tamerlane"]]),
    Not(review[s_idx["ONeill"]][p_idx["Tamerlane"]])
)

# Option B: Kramer, O'Neill
opt_b = And(
    Not(review[s_idx["Jiang"]][p_idx["Tamerlane"]]),
    review[s_idx["Kramer"]][p_idx["Tamerlane"]],
    Not(review[s_idx["Lopez"]][p_idx["Tamerlane"]]),
    Not(review[s_idx["Megregian"]][p_idx["Tamerlane"]]),
    review[s_idx["ONeill"]][p_idx["Tamerlane"]]
)

# Option C: Kramer, Lopez, O'Neill
opt_c = And(
    Not(review[s_idx["Jiang"]][p_idx["Tamerlane"]]),
    review[s_idx["Kramer"]][p_idx["Tamerlane"]],
    review[s_idx["Lopez"]][p_idx["Tamerlane"]],
    Not(review[s_idx["Megregian"]][p_idx["Tamerlane"]]),
    review[s_idx["ONeill"]][p_idx["Tamerlane"]]
)

# Option D: Kramer, Megregian, O'Neill
opt_d = And(
    Not(review[s_idx["Jiang"]][p_idx["Tamerlane"]]),
    review[s_idx["Kramer"]][p_idx["Tamerlane"]],
    Not(review[s_idx["Lopez"]][p_idx["Tamerlane"]]),
    review[s_idx["Megregian"]][p_idx["Tamerlane"]],
    review[s_idx["ONeill"]][p_idx["Tamerlane"]]
)

# Option E: Lopez, Megregian, O'Neill
opt_e = And(
    Not(review[s_idx["Jiang"]][p_idx["Tamerlane"]]),
    Not(review[s_idx["Kramer"]][p_idx["Tamerlane"]]),
    review[s_idx["Lopez"]][p_idx["Tamerlane"]],
    review[s_idx["Megregian"]][p_idx["Tamerlane"]],
    review[s_idx["ONeill"]][p_idx["Tamerlane"]]
)

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