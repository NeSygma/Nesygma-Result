from z3 import *

# Declare variables for each item
days = range(1, 7)  # 1..6
H = Int('H')  # harmonica
L = Int('L')  # lamp
M = Int('M')  # mirror
S = Int('S')  # sundial
T = Int('T')  # table
V = Int('V')  # vase

solver = Solver()
# Domain constraints
for var in [H, L, M, S, T, V]:
    solver.add(var >= 1, var <= 6)
# All different
solver.add(Distinct(H, L, M, S, T, V))
# Base constraints
solver.add(S != 1)  # sundial not on June 1
# If H earlier than L then M earlier than L: (H < L) => (M < L)
solver.add(Or(H >= L, M < L))
# Sundial earlier than mirror and vase
solver.add(S < M)
solver.add(S < V)
# Table earlier than H xor earlier than V (not both)
# XOR: (T < H) != (T < V)
solver.add(Or(And(T < H, Not(T < V)), And(Not(T < H), T < V)))
# Extra condition: Table later than both mirror and vase
solver.add(T > M)
solver.add(T > V)

# Define option constraints
opt_a = H < T  # A
opt_b = T < L  # B
opt_c = T < S  # C
opt_d = M < V  # D
opt_e = S < L  # E

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

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