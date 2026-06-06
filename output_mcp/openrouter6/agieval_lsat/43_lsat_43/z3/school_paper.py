from z3 import *

solver = Solver()

# Students: 0: Jiang, 1: Kramer, 2: Lopez, 3: Megregian, 4: O'Neill
S = [Bool(f"S_{i}") for i in range(5)]
T = [Bool(f"T_{i}") for i in range(5)]
U = [Bool(f"U_{i}") for i in range(5)]

# Base constraints

# 1. Each student reviews at least one play
for i in range(5):
    solver.add(Or(S[i], T[i], U[i]))

# 2. Kramer and Lopez each review fewer plays than Megregian
count = [If(S[i], 1, 0) + If(T[i], 1, 0) + If(U[i], 1, 0) for i in range(5)]
solver.add(count[1] < count[3])  # Kramer < Megregian
solver.add(count[2] < count[3])  # Lopez < Megregian

# 3. Neither Lopez nor Megregian reviews any play Jiang reviews
for play in [S, T, U]:
    solver.add(Not(And(play[0], play[2])))  # Jiang and Lopez
    solver.add(Not(And(play[0], play[3])))  # Jiang and Megregian

# 4. Kramer and O'Neill both review Tamerlane
solver.add(T[1])  # Kramer
solver.add(T[4])  # O'Neill

# 5. Exactly two students have identical review sets
pairs = []
for i in range(5):
    for j in range(i+1, 5):
        eq = And(S[i] == S[j], T[i] == T[j], U[i] == U[j])
        pairs.append(eq)
solver.add(Sum(pairs) == 1)

# Now evaluate each answer choice
found_options = []

# Answer choices mapping to sets of student indices
choices = [
    ("A", [2]),               # Lopez
    ("B", [4]),               # O'Neill
    ("C", [0, 2]),            # Jiang, Lopez
    ("D", [1, 4]),            # Kramer, O'Neill
    ("E", [2, 3])             # Lopez, Megregian
]

for letter, indices in choices:
    solver.push()
    # Add constraints that exactly these students review only Sunset
    for i in range(5):
        if i in indices:
            # Student i reviews only Sunset
            solver.add(S[i])
            solver.add(Not(T[i]))
            solver.add(Not(U[i]))
        else:
            # Student i does NOT review only Sunset
            solver.add(Or(Not(S[i]), T[i], U[i]))
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