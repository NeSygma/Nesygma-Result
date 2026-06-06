from z3 import *

# Create solver
solver = Solver()

# Define time slots for each member (1-6)
G = Int('Guitarist')
K = Int('Keyboard')
P = Int('Percussionist')
S = Int('Saxophonist')
T = Int('Trumpeter')
V = Int('Violinist')

members = [G, K, P, S, T, V]

# Base constraints
# 1. Each member gets a distinct time slot (1-6)
for m in members:
    solver.add(m >= 1, m <= 6)
solver.add(Distinct(members))

# 2. Guitarist does not perform the fourth solo
solver.add(G != 4)

# 3. Percussionist before keyboard player
solver.add(P < K)

# 4. Violinist before keyboard player before guitarist
solver.add(V < K)
solver.add(K < G)

# 5. Saxophonist after either percussionist or trumpeter, but not both
# (S > P XOR S > T) means exactly one of these is true
# We'll encode as: (S > P and S <= T) OR (S <= P and S > T)
solver.add(Or(
    And(S > P, S <= T),
    And(S <= P, S > T)
))

# Now evaluate each option
# Option A: The keyboard player performs the first solo
opt_a = (K == 1)

# Option B: The guitarist performs the second solo
opt_b = (G == 2)

# Option C: The guitarist performs a solo at some time before the saxophonist does
opt_c = (G < S)

# Option D: The guitarist performs a solo at some time before the percussionist does
opt_d = (G < P)

# Option E: The keyboard player performs a solo at some time before the saxophonist does
opt_e = (K < S)

# Test each option
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