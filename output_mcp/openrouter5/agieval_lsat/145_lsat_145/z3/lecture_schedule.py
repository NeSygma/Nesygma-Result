from z3 import *

# We have 4 lectures, positions 0,1,2,3 (earliest to latest)
# Topics: lithographs (L), oil paintings (O), sculptures (S), watercolors (W)
# Historians: Farley (F), Garcia (G), Holden (H), Jiang (J)

# We'll assign each topic and each historian a position (0-3)
L, O, S, W = Ints('L O S W')
F, G, H, J = Ints('F G H J')

solver = Solver()

# All positions are between 0 and 3
for var in [L, O, S, W, F, G, H, J]:
    solver.add(var >= 0, var <= 3)

# Each topic has a distinct position
solver.add(Distinct(L, O, S, W))

# Each historian has a distinct position
solver.add(Distinct(F, G, H, J))

# Constraints:
# 1. Oil paintings and watercolors must both be earlier than lithographs
solver.add(O < L)
solver.add(W < L)

# 2. Farley's lecture must be earlier than the oil paintings lecture
solver.add(F < O)

# 3. Holden's lecture must be earlier than both Garcia's and Jiang's lectures
solver.add(H < G)
solver.add(H < J)

# Now evaluate each option
# Option A: Farley's lecture is earlier than the sculptures lecture
opt_a = (F < S)

# Option B: Holden's lecture is earlier than the lithographs lecture
opt_b = (H < L)

# Option C: The sculptures lecture is earlier than Garcia's lecture
opt_c = (S < G)

# Option D: The sculptures lecture is earlier than Jiang's lecture
opt_d = (S < J)

# Option E: The watercolors lecture is earlier than Garcia's lecture
opt_e = (W < G)

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