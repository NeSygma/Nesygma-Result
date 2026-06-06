from z3 import *

# Define solver and base constraints
solver = Solver()
# Variables for each item day (1..6)
H = Int('H')
L = Int('L')
M = Int('M')
S = Int('S')
T = Int('T')
V = Int('V')
vars = [H, L, M, S, T, V]
for v in vars:
    solver.add(v >= 1, v <= 6)
# All distinct
solver.add(Distinct(vars))
# Constraint 1: S not on day 1
solver.add(S != 1)
# Constraint 2: If H earlier than L then M earlier than L
solver.add(Implies(H < L, M < L))
# Constraint 3: S earlier than M and V
solver.add(S < M)
solver.add(S < V)
# Constraint 4: T earlier than H xor earlier than V (exactly one)
solver.add(Xor(T < H, T < V))

# Define option constraints
opt_a = And(S == 5)
opt_b = And(S == 4)
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