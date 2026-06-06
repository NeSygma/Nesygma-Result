from z3 import *

# Students: Jiang (0), Kramer (1), Lopez (2), Megregian (3), O'Neill (4)
# Plays: Sunset (0), Tamerlane (1), Undulation (2)
# Each student reviews at least one play.
# S[student][play] is a boolean variable.

S = [[Bool(f'S_{i}_{j}') for j in range(3)] for i in range(5)]

solver = Solver()

# Each student reviews at least one play.
for i in range(5):
    solver.add(Or([S[i][j] for j in range(3)]))

def count_plays(i):
    return Sum([If(S[i][j], 1, 0) for j in range(3)])

# Condition 1: Kramer and Lopez each review fewer plays than Megregian.
solver.add(count_plays(1) < count_plays(3))
solver.add(count_plays(2) < count_plays(3))

# Condition 2: Neither Lopez nor Megregian reviews any play Jiang reviews.
for j in range(3):
    solver.add(Implies(S[0][j], And(Not(S[2][j]), Not(S[3][j]))))

# Condition 3: Kramer and O'Neill both review Tamerlane (play 1).
solver.add(S[1][1])
solver.add(S[4][1])

# Condition 4: Exactly two of the students review exactly the same play or plays as each other.
# Two students i and j have the same set of plays if S[i][p] == S[j][p] for all p.
def same_set(i, j):
    return And([S[i][p] == S[j][p] for p in range(3)])

pairs = []
for i in range(5):
    for j in range(i + 1, 5):
        pairs.append(same_set(i, j))

# Exactly one pair is equal:
solver.add(Sum([If(p, 1, 0) for p in pairs]) == 1)

# Define the answer choices
# (A) Jiang reviews more of the plays than Lopez does.
# (B) Megregian reviews more of the plays than Jiang does.
# (C) Megregian reviews more of the plays than O'Neill does.
# (D) O'Neill reviews more of the plays than Jiang does.
# (E) O'Neill reviews more of the plays than Kramer does.

choices = [
    ("A", count_plays(0) > count_plays(2)),
    ("B", count_plays(3) > count_plays(0)),
    ("C", count_plays(3) > count_plays(4)),
    ("D", count_plays(4) > count_plays(0)),
    ("E", count_plays(4) > count_plays(1))
]

found_options = []
for letter, constr in choices:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
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