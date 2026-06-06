from z3 import *

solver = Solver()

# Declare variables for each antique (day number 1..6)
H, L, M, S, T, V = Ints('H L M S T V')

# Base constraints
# All days distinct
solver.add(Distinct([H, L, M, S, T, V]))
# Each day between 1 and 6
for var in [H, L, M, S, T, V]:
    solver.add(var >= 1, var <= 6)

# Constraint 1: Sundial not on June 1
solver.add(S != 1)

# Constraint 2: If harmonica earlier than lamp, then mirror earlier than lamp
# (H < L) => (M < L)
solver.add(Implies(H < L, M < L))

# Constraint 3: Sundial earlier than mirror and earlier than vase
solver.add(S < M)
solver.add(S < V)

# Constraint 4: Table earlier than harmonica XOR earlier than vase
solver.add((T < H) != (T < V))

# Now test each option: which antique CANNOT be immediately before vase?
# We'll test by adding constraint X + 1 == V and checking satisfiability.
# If unsat, then X cannot be immediately before V.

found_options = []
for letter, antique in [("A", H), ("B", L), ("C", M), ("D", S), ("E", T)]:
    solver.push()
    solver.add(antique + 1 == V)
    if solver.check() == unsat:   # Note: changed from sat to unsat to collect impossible options
        found_options.append(letter)
    solver.pop()

# According to the skeleton, we print answer if exactly one found_options
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")