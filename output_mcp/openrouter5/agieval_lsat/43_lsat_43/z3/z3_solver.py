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

# Create variables
R = [[Bool(f"R_{students[i]}_{plays[j]}") for j in range(3)] for i in range(5)]

solver = Solver()

# 1. Each student reviews one or more plays (non-empty set)
for i in range(5):
    solver.add(Or([R[i][j] for j in range(3)]))

# 2. Kramer and Lopez each review fewer of the plays than Megregian.
# Count how many plays each reviews.
kramer_count = Sum([If(R[s_idx["Kramer"]][j], 1, 0) for j in range(3)])
lopez_count = Sum([If(R[s_idx["Lopez"]][j], 1, 0) for j in range(3)])
megregian_count = Sum([If(R[s_idx["Megregian"]][j], 1, 0) for j in range(3)])

solver.add(kramer_count < megregian_count)
solver.add(lopez_count < megregian_count)

# 3. Neither Lopez nor Megregian reviews any play Jiang reviews.
# For each play, if Jiang reviews it, then Lopez does not and Megregian does not.
for j in range(3):
    solver.add(Implies(R[s_idx["Jiang"]][j], Not(R[s_idx["Lopez"]][j])))
    solver.add(Implies(R[s_idx["Jiang"]][j], Not(R[s_idx["Megregian"]][j])))

# 4. Kramer and O'Neill both review Tamerlane.
solver.add(R[s_idx["Kramer"]][p_idx["Tamerlane"]])
solver.add(R[s_idx["ONeill"]][p_idx["Tamerlane"]])

# 5. Exactly two of the students review exactly the same play or plays as each other.
# That means there is exactly one pair of students who have identical review sets,
# and no other pair has identical sets.

# For each pair (i1, i2), define whether they have identical review sets.
# Two students have identical sets iff for each play, they both review it or both don't.
pair_vars = []
pair_info = []
for i1 in range(5):
    for i2 in range(i1+1, 5):
        same = Bool(f"same_{students[i1]}_{students[i2]}")
        pair_vars.append(same)
        pair_info.append((i1, i2))
        # same is true iff for all j, R[i1][j] == R[i2][j]
        solver.add(same == And([R[i1][j] == R[i2][j] for j in range(3)]))

# Exactly two students have identical sets => exactly one pair is True
solver.add(Sum([If(v, 1, 0) for v in pair_vars]) == 1)

# Now evaluate each answer choice.
# Each choice is: "the students who review only Sunset" — meaning they review Sunset and do NOT review Tamerlane or Undulation.
# So for a student to be in the "only Sunset" set, they must review Sunset, not Tamerlane, not Undulation.

# Option A: Lopez
opt_a = And(R[s_idx["Lopez"]][p_idx["Sunset"]],
            Not(R[s_idx["Lopez"]][p_idx["Tamerlane"]]),
            Not(R[s_idx["Lopez"]][p_idx["Undulation"]]))

# Option B: O'Neill
opt_b = And(R[s_idx["ONeill"]][p_idx["Sunset"]],
            Not(R[s_idx["ONeill"]][p_idx["Tamerlane"]]),
            Not(R[s_idx["ONeill"]][p_idx["Undulation"]]))

# Option C: Jiang, Lopez
opt_c = And(
    And(R[s_idx["Jiang"]][p_idx["Sunset"]],
        Not(R[s_idx["Jiang"]][p_idx["Tamerlane"]]),
        Not(R[s_idx["Jiang"]][p_idx["Undulation"]])),
    And(R[s_idx["Lopez"]][p_idx["Sunset"]],
        Not(R[s_idx["Lopez"]][p_idx["Tamerlane"]]),
        Not(R[s_idx["Lopez"]][p_idx["Undulation"]]))
)

# Option D: Kramer, O'Neill
opt_d = And(
    And(R[s_idx["Kramer"]][p_idx["Sunset"]],
        Not(R[s_idx["Kramer"]][p_idx["Tamerlane"]]),
        Not(R[s_idx["Kramer"]][p_idx["Undulation"]])),
    And(R[s_idx["ONeill"]][p_idx["Sunset"]],
        Not(R[s_idx["ONeill"]][p_idx["Tamerlane"]]),
        Not(R[s_idx["ONeill"]][p_idx["Undulation"]]))
)

# Option E: Lopez, Megregian
opt_e = And(
    And(R[s_idx["Lopez"]][p_idx["Sunset"]],
        Not(R[s_idx["Lopez"]][p_idx["Tamerlane"]]),
        Not(R[s_idx["Lopez"]][p_idx["Undulation"]])),
    And(R[s_idx["Megregian"]][p_idx["Sunset"]],
        Not(R[s_idx["Megregian"]][p_idx["Tamerlane"]]),
        Not(R[s_idx["Megregian"]][p_idx["Undulation"]]))
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