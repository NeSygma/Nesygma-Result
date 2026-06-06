from z3 import *

solver = Solver()

# Students: Jiang(0), Kramer(1), Lopez(2), Megregian(3), O'Neill(4)
# Plays: Sunset(0), Tamerlane(1), Undulation(2)

# Boolean variables: student i reviews play j
reviews = [[Bool(f"reviews_{i}_{j}") for j in range(3)] for i in range(5)]

# Each student reviews at least one play
for i in range(5):
    solver.add(Or(reviews[i][0], reviews[i][1], reviews[i][2]))

# Count of plays each student reviews
count = [Int(f"count_{i}") for i in range(5)]
for i in range(5):
    solver.add(count[i] == Sum([If(reviews[i][j], 1, 0) for j in range(3)]))

# Condition 1: Kramer and Lopez each review fewer plays than Megregian
solver.add(count[1] < count[3])  # Kramer < Megregian
solver.add(count[2] < count[3])  # Lopez < Megregian

# Condition 2: Neither Lopez nor Megregian reviews any play Jiang reviews
# For each play, if Jiang reviews it, then Lopez and Megregian don't
for j in range(3):
    solver.add(Implies(reviews[0][j], Not(reviews[2][j])))  # Jiang -> not Lopez
    solver.add(Implies(reviews[0][j], Not(reviews[3][j])))  # Jiang -> not Megregian

# Condition 3: Kramer and O'Neill both review Tamerlane
solver.add(reviews[1][1] == True)   # Kramer reviews Tamerlane
solver.add(reviews[4][1] == True)   # O'Neill reviews Tamerlane

# Condition 4: Exactly two students review exactly the same play(s)
# We need to check all pairs and count how many pairs have identical review sets
same_reviews = []
for i in range(5):
    for k in range(i+1, 5):
        pair_same = And([reviews[i][j] == reviews[k][j] for j in range(3)])
        same_reviews.append(pair_same)

# Exactly one pair has same reviews (meaning exactly 2 students share the same set)
solver.add(Sum([If(s, 1, 0) for s in same_reviews]) == 1)

# Additional condition: Jiang does NOT review Tamerlane
solver.add(reviews[0][1] == False)

# Now test each answer choice
# (A) Jiang reviews Sunset
opt_a = reviews[0][0]

# (B) Lopez reviews Undulation
opt_b = reviews[2][2]

# (C) Megregian reviews Sunset
opt_c = reviews[3][0]

# (D) Megregian reviews Tamerlane
opt_d = reviews[3][1]

# (E) O'Neill reviews Undulation
opt_e = reviews[4][2]

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