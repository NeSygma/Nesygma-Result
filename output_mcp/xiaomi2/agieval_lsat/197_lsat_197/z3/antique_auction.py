from z3 import *

solver = Solver()

# Variables: day assigned to each antique (1-6)
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

# Constraint 4: (T < H) XOR (T < V)
solver.add(Xor(T < H, T < V))

# Define option constraints
opt_a = And(T == 2, L == 3)
opt_b = And(S == 2, V == 3)
opt_c = And(M == 3, S == 4)
opt_d = And(V == 4, S == 5)
opt_e = And(S == 4, T == 5)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT: H={m[H]}, L={m[L]}, M={m[M]}, S={m[S]}, T={m[T]}, V={m[V]}")
    else:
        print(f"Option {letter} is UNSAT")
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