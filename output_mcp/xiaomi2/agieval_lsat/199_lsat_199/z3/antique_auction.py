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

# Now check each option: can that antique immediately precede the vase?
# Option A: Harmonica immediately precedes Vase (H + 1 == V)
# Option B: Lamp immediately precedes Vase (L + 1 == V)
# Option C: Mirror immediately precedes Vase (M + 1 == V)
# Option D: Sundial immediately precedes Vase (S + 1 == V)
# Option E: Table immediately precedes Vase (T + 1 == V)

options = [
    ("A", H + 1 == V),
    ("B", L + 1 == V),
    ("C", M + 1 == V),
    ("D", S + 1 == V),
    ("E", T + 1 == V),
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        m = solver.model()
        found_options.append(letter)
        print(f"Option {letter} is SAT: H={m[H]}, L={m[L]}, M={m[M]}, S={m[S]}, T={m[T]}, V={m[V]}")
    else:
        print(f"Option {letter} is UNSAT (cannot precede vase)")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")