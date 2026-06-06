from z3 import *

solver = Solver()

# Variables: each antique assigned a day (1-6)
H = Int('H')  # Harmonica
L = Int('L')  # Lamp
M = Int('M')  # Mirror
S = Int('S')  # Sundial
T = Int('T')  # Table
V = Int('V')  # Vase

antiques = [H, L, M, S, T, V]

# Each antique on a different day, days 1-6
for a in antiques:
    solver.add(a >= 1, a <= 6)
solver.add(Distinct(antiques))

# Constraint 1: Sundial not on June 1st
solver.add(S != 1)

# Constraint 2: If H < L then M < L
solver.add(Implies(H < L, M < L))

# Constraint 3: S < M and S < V
solver.add(S < M)
solver.add(S < V)

# Constraint 4: (T < H or T < V) but not both (XOR)
solver.add(Or(And(T < H, Not(T < V)), And(Not(T < H), T < V)))

# The question: which CANNOT immediately precede the vase?
# We check each option: can that antique immediately precede the vase?
# The one that CANNOT (UNSAT) is the answer.

options = [
    ("A", H + 1 == V),  # Harmonica
    ("B", L + 1 == V),  # Lamp
    ("C", M + 1 == V),  # Mirror
    ("D", S + 1 == V),  # Sundial
    ("E", T + 1 == V),  # Table
]

cannot_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
        cannot_options.append(letter)
    solver.pop()

if len(cannot_options) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_options[0]}")
elif len(cannot_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple CANNOT options found {cannot_options}")
else:
    print("STATUS: unsat")
    print("Refine: No CANNOT options found")