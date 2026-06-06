from z3 import *

solver = Solver()

# Students: Jiang(0), Kramer(1), Lopez(2), Megregian(3), O'Neill(4)
# Plays: Sunset(0), Tamerlane(1), Undulation(2)

# Boolean variables: reviews[s][p] = True if student s reviews play p
reviews = [[Bool(f"reviews_{s}_{p}") for p in range(3)] for s in range(5)]

# Each student reviews at least one play
for s in range(5):
    solver.add(Or(reviews[s][0], reviews[s][1], reviews[s][2]))

# Count of plays each student reviews
count = [Int(f"count_{s}") for s in range(5)]
for s in range(5):
    solver.add(count[s] == Sum([If(reviews[s][p], 1, 0) for p in range(3)]))

# Condition 1: Kramer and Lopez each review fewer plays than Megregian
solver.add(count[1] < count[3])  # Kramer < Megregian
solver.add(count[2] < count[3])  # Lopez < Megregian

# Condition 2: Neither Lopez nor Megregian reviews any play Jiang reviews
for p in range(3):
    solver.add(Implies(reviews[0][p], Not(reviews[2][p])))  # Jiang -> not Lopez
    solver.add(Implies(reviews[0][p], Not(reviews[3][p])))  # Jiang -> not Megregian

# Condition 3: Kramer and O'Neill both review Tamerlane
solver.add(reviews[1][1] == True)  # Kramer reviews Tamerlane
solver.add(reviews[4][1] == True)  # O'Neill reviews Tamerlane

# Condition 4: Exactly two of the students review exactly the same play or plays as each other
# This means exactly one pair of students has identical review sets, and all other pairs differ
# We need to check all pairs
same = [[Bool(f"same_{i}_{j}") for j in range(5)] for i in range(5)]
for i in range(5):
    for j in range(5):
        if i < j:
            # same[i][j] iff they review exactly the same plays
            solver.add(same[i][j] == And([reviews[i][p] == reviews[j][p] for p in range(3)]))
        elif i == j:
            solver.add(same[i][j] == True)
        else:
            solver.add(same[i][j] == same[j][i])

# Exactly one pair (i,j) with i<j has same[i][j] = True
pair_same = [same[i][j] for i in range(5) for j in range(i+1, 5)]
solver.add(Sum([If(s, 1, 0) for s in pair_same]) == 1)

# Additional condition: Exactly three of the students review Undulation
solver.add(Sum([If(reviews[s][2], 1, 0) for s in range(5)]) == 3)

# Now test each option
# (A) Megregian does not review Undulation
opt_a = Not(reviews[3][2])
# (B) O'Neill does not review Undulation
opt_b = Not(reviews[4][2])
# (C) Jiang reviews Undulation
opt_c = reviews[0][2]
# (D) Lopez reviews Tamerlane
opt_d = reviews[2][1]
# (E) O'Neill reviews Sunset
opt_e = reviews[4][0]

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