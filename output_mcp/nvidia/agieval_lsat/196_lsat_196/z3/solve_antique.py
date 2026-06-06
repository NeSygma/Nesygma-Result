from z3 import *

solver = Solver()

# Declare position variables for each antique
H = Int('H')  # harmonica
L = Int('L')  # lamp
M = Int('M')  # mirror
S = Int('S')  # sundial
T = Int('T')  # table
V = Int('V')  # vase

# All positions must be distinct (a permutation of 0..5)
solver.add(Distinct([H, L, M, S, T, V]))

# Domain constraints: each position is 0 (June 1) through 5 (June 6)
for var in [H, L, M, S, T, V]:
    solver.add(var >= 0, var <= 5)

# Constraint 1: Sundial is not on June 1st (position 0)
solver.add(S != 0)

# Constraint 2: If H is earlier than L then M is earlier than L
solver.add(Or(H >= L, M < L))

# Constraint 3: Sundial is earlier than both mirror and vase
solver.add(S < M, S < V)

# Constraint 4: Table is earlier than exactly one of H or V (XOR)
solver.add(Xor(T < H, T < V))

# Option-specific constraints (encode the full ordering for each choice)
opt_a_constr = And(
    H == 0,  # A: harmonica on day 1
    T == 1,  # table on day 2
    S == 2,  # sundial on day 3
    L == 3,  # lamp on day 4
    V == 4,  # vase on day 5
    M == 5   # mirror on day 6
)

opt_b_constr = And(
    L == 0,  # B: lamp on day 1
    H == 1,  # harmonica on day 2
    S == 2,  # sundial on day 3
    M == 3,  # mirror on day 4
    V == 4,  # vase on day 5
    T == 5   # table on day 6
)

opt_c_constr = And(
    H == 0,  # C: harmonica on day 1
    S == 1,  # sundial on day 2
    T == 2,  # table on day 3
    M == 3,  # mirror on day 4
    L == 4,  # lamp on day 5
    V == 5   # vase on day 6
)

opt_d_constr = And(
    S == 0,  # D: sundial on day 1 (violates constraint 1, but kept for completeness)
    M == 1,  # mirror on day 2
    H == 2,  # harmonica on day 3
    T == 3,  # table on day 4
    V == 4,  # vase on day 5
    L == 5   # lamp on day 6
)

opt_e_constr = And(
    V == 0,  # E: vase on day 1
    S == 1,  # sundial on day 2
    L == 2,  # lamp on day 3
    H == 3,  # harmonica on day 4
    T == 4,  # table on day 5
    M == 5   # mirror on day 6
)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output according to the required multiple‑choice skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")