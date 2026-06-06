from z3 import *

solver = Solver()

# Variables: day assigned to each antique (1-6)
H = Int('H')  # Harmonica
L = Int('L')  # Lamp
M = Int('M')  # Mirror
S = Int('S')  # Sundial
T = Int('T')  # Table
V = Int('V')  # Vase

all_vars = [H, L, M, S, T, V]

# Each antique on a unique day from 1 to 6
for v in all_vars:
    solver.add(v >= 1, v <= 6)
solver.add(Distinct(all_vars))

# Constraint 1: Sundial not on June 1st
solver.add(S != 1)

# Constraint 2: If H < L then M < L
solver.add(Implies(H < L, M < L))

# Constraint 3: S < M and S < V
solver.add(S < M)
solver.add(S < V)

# Constraint 4: (T < H or T < V) but not both (XOR)
solver.add(Xor(T < H, T < V))

# Additional premise: T > M and T > V (table later than both mirror and vase)
solver.add(T > M)
solver.add(T > V)

# Define answer choice constraints
opt_a = (H < T)   # Harmonica earlier than Table
opt_b = (T < L)   # Table earlier than Lamp
opt_c = (T < S)   # Table earlier than Sundial
opt_d = (M < V)   # Mirror earlier than Vase
opt_e = (S < L)   # Sundial earlier than Lamp

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        m = solver.model()
        found_options.append(letter)
        print(f"Option {letter} is SAT: H={m[H]}, L={m[L]}, M={m[M]}, S={m[S]}, T={m[T]}, V={m[V]}")
    else:
        print(f"Option {letter} is UNSAT")
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