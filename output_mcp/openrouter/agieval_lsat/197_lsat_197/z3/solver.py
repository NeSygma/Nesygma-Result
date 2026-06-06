from z3 import *

# Create solver and variables
solver = Solver()
# Items
H = Int('H')  # harmonica
L = Int('L')  # lamp
M = Int('M')  # mirror
S = Int('S')  # sundial
T = Int('T')  # table
V = Int('V')  # vase
items = [H, L, M, S, T, V]
# Domain constraints: each day 1..6
for var in items:
    solver.add(var >= 1, var <= 6)
# All distinct
solver.add(Distinct(items))
# Base constraints
# 1. Sundial not on June 1
solver.add(S != 1)
# 2. If H earlier than L then M earlier than L
solver.add(Or(H >= L, M < L))
# 3. Sundial earlier than Mirror and Vase
solver.add(S < M)
solver.add(S < V)
# 4. Table earlier than H xor earlier than V (exactly one)
solver.add(Xor(T < H, T < V))

# Option specific constraints
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