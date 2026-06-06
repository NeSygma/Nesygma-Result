from z3 import *

solver = Solver()

# Declare variables for each antique's auction day
H = Int('H')  # harmonica
L = Int('L')  # lamp
M = Int('M')  # mirror
S = Int('S')  # sundial
T = Int('T')  # table
V = Int('V')  # vase

# Domain constraints: each day between 1 and 6
solver.add(1 <= H, H <= 6)
solver.add(1 <= L, L <= 6)
solver.add(1 <= M, M <= 6)
solver.add(1 <= S, S <= 6)
solver.add(1 <= T, T <= 6)
solver.add(1 <= V, V <= 6)

# All distinct: each day has exactly one antique
solver.add(Distinct([H, L, M, S, T, V]))

# Condition 1: Sundial not on June 1st
solver.add(S != 1)

# Condition 2: If harmonica earlier than lamp, then mirror earlier than lamp
solver.add(Or(H >= L, M < L))

# Condition 3: Sundial earlier than mirror and earlier than vase
solver.add(S < M)
solver.add(S < V)

# Condition 4: Table earlier than harmonica or earlier than vase, but not both
solver.add(Xor(T < H, T < V))

# Now evaluate each answer choice
found_options = []

# Option A: Table on June 2nd, Lamp on June 3rd
opt_a = And(T == 2, L == 3)
# Option B: Sundial on June 2nd, Vase on June 3rd
opt_b = And(S == 2, V == 3)
# Option C: Mirror on June 3rd, Sundial on June 4th
opt_c = And(M == 3, S == 4)
# Option D: Vase on June 4th, Sundial on June 5th
opt_d = And(V == 4, S == 5)
# Option E: Sundial on June 4th, Table on June 5th
opt_e = And(S == 4, T == 5)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        # Optionally print the model for this option
        # m = solver.model()
        # print(f"Option {letter} model: H={m[H]}, L={m[L]}, M={m[M]}, S={m[S]}, T={m[T]}, V={m[V]}")
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