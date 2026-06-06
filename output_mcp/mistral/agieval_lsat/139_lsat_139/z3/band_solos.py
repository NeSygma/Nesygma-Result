from z3 import *

# BENCHMARK_MODE is ON for this problem
BENCHMARK_MODE = True

# Create a solver
solver = Solver()

# Declare symbolic variables for each band member's solo position
# Positions are 1 to 6 (1 = first, 6 = last)
G = Int('G')  # guitarist
K = Int('K')  # keyboard player
P = Int('P')  # percussionist
S = Int('S')  # saxophonist
T = Int('T')  # trumpeter
V = Int('V')  # violinist

# Each position is unique and between 1 and 6
positions = [G, K, P, S, T, V]
for pos in positions:
    solver.add(And(pos >= 1, pos <= 6))

# Constraint 1: Guitarist does not perform the 4th solo
solver.add(G != 4)

# Constraint 2: Percussionist performs before keyboard player
solver.add(P < K)

# Constraint 3: Keyboard player performs after violinist and before guitarist
solver.add(V < K)
solver.add(K < G)

# Constraint 4: Saxophonist performs after either percussionist or trumpeter, but not both
# This means: (S > P and S <= T) or (S > T and S <= P)
solver.add(Or(And(S > P, S <= T), And(S > T, S <= P)))

# All positions must be distinct
solver.add(Distinct(positions))

# Now test each multiple-choice option
found_options = []

# Option A: violinist, percussionist, saxophonist, guitarist, trumpeter, keyboard player
# V=1, P=2, S=3, G=4, T=5, K=6
opt_a_constr = And(
    V == 1,
    P == 2,
    S == 3,
    G == 4,
    T == 5,
    K == 6
)

# Option B: percussionist, violinist, keyboard player, trumpeter, saxophonist, guitarist
# P=1, V=2, K=3, T=4, S=5, G=6
opt_b_constr = And(
    P == 1,
    V == 2,
    K == 3,
    T == 4,
    S == 5,
    G == 6
)

# Option C: violinist, trumpeter, saxophonist, percussionist, keyboard player, guitarist
# V=1, T=2, S=3, P=4, K=5, G=6
opt_c_constr = And(
    V == 1,
    T == 2,
    S == 3,
    P == 4,
    K == 5,
    G == 6
)

# Option D: keyboard player, trumpeter, violinist, saxophonist, guitarist, percussionist
# K=1, T=2, V=3, S=4, G=5, P=6
opt_d_constr = And(
    K == 1,
    T == 2,
    V == 3,
    S == 4,
    G == 5,
    P == 6
)

# Option E: guitarist, violinist, keyboard player, percussionist, saxophonist, trumpeter
# G=1, V=2, K=3, P=4, S=5, T=6
opt_e_constr = And(
    G == 1,
    V == 2,
    K == 3,
    P == 4,
    S == 5,
    T == 6
)

# Test each option
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")