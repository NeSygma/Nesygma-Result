from z3 import *

solver = Solver()

# Variables: day assignment for each antique (1-6)
H = Int('H')  # Harmonica
L = Int('L')  # Lamp
M = Int('M')  # Mirror
S = Int('S')  # Sundial
T = Int('T')  # Table
V = Int('V')  # Vase

antiques = [H, L, M, S, T, V]

# Each antique assigned to a day 1-6, all different
for a in antiques:
    solver.add(a >= 1, a <= 6)
solver.add(Distinct(antiques))

# Constraint 1: Sundial not on June 1st
solver.add(S != 1)

# Constraint 2: If H < L, then M < L
solver.add(Implies(H < L, M < L))

# Constraint 3: S < M and S < V
solver.add(S < M)
solver.add(S < V)

# Constraint 4: (T < H OR T < V) but NOT both (XOR)
solver.add(Or(And(T < H, Not(T < V)), And(Not(T < H), T < V)))

# Define option constraints
opt_a = (S == 5)
opt_b = (S == 4)
opt_c = And(L == 5, M == 6)
opt_d = And(T == 3, L == 4)
opt_e = And(H == 2, V == 3)

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