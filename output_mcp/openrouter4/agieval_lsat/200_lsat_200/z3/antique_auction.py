from z3 import *

solver = Solver()

# Days: 1 to 6
# Variables for each antique
H, L, M, S, T, V = Ints('H L M S T V')

# Domains: each day is between 1 and 6
days = [H, L, M, S, T, V]
for d in days:
    solver.add(1 <= d, d <= 6)

# All distinct (each day one antique, each antique one day)
solver.add(Distinct(days))

# Constraint 1: Sundial not on June 1st
solver.add(S != 1)

# Constraint 2: If H < L then M < L
solver.add(Implies(H < L, M < L))

# Constraint 3: S < M and S < V
solver.add(S < M)
solver.add(S < V)

# Constraint 4: Table earlier than harmonica OR earlier than vase, but not both
# (T < H) XOR (T < V)
solver.add(Xor(T < H, T < V))

# Options
options = [
    ("A", M == 2),
    ("B", L == 2),
    ("C", V == 2),
    ("D", L == 3),
    ("E", M == 5)
]

found_options = []
for letter, constr in options:
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