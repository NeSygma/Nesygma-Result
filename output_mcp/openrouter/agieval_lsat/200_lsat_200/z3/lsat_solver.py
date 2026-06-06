from z3 import *

solver = Solver()
# Variables for each item
days = range(1,7)
H = Int('H')
L = Int('L')
M = Int('M')
S = Int('S')
T = Int('T')
V = Int('V')
vars = [H,L,M,S,T,V]
# domain constraints
for v in vars:
    solver.add(v >= 1, v <= 6)
# all distinct
solver.add(Distinct(vars))
# Constraint 1: S not on day 1
solver.add(S != 1)
# Constraint 2: If H < L then M < L
solver.add(Implies(H < L, M < L))
# Constraint 3: S earlier than M and V
solver.add(S < M)
solver.add(S < V)
# Constraint 4: T earlier than H xor earlier than V (exactly one)
# XOR can be expressed as (T < H) != (T < V)
solver.add((T < H) != (T < V))

# Define option constraints
opt_constraints = []
# A: M == 2
opt_constraints.append(("A", M == 2))
# B: L == 2
opt_constraints.append(("B", L == 2))
# C: V == 2
opt_constraints.append(("C", V == 2))
# D: L == 3
opt_constraints.append(("D", L == 3))
# E: M == 5
opt_constraints.append(("E", M == 5))

found_options = []
for letter, constr in opt_constraints:
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