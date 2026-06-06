from z3 import *

# We have 4 positions (1st, 2nd, 3rd, 4th)
# Topics: lithographs (L), oil paintings (O), sculptures (S), watercolors (W)
# Historians: Farley (F), Garcia (G), Holden (H), Jiang (J)

# We'll use integer variables for positions (1-4)
# Each topic gets a position
L = Int('L')  # lithographs
O = Int('O')  # oil paintings
S = Int('S')  # sculptures
W = Int('W')  # watercolors

# Each historian gets a position
F = Int('F')  # Farley
G = Int('G')  # Garcia
H = Int('H')  # Holden
J = Int('J')  # Jiang

solver = Solver()

# Domain: positions 1 through 4
all_vars = [L, O, S, W, F, G, H, J]
for v in all_vars:
    solver.add(v >= 1, v <= 4)

# All topics distinct
solver.add(Distinct(L, O, S, W))

# All historians distinct
solver.add(Distinct(F, G, H, J))

# Constraints:
# 1. Oil paintings and watercolors must both be earlier than lithographs.
solver.add(O < L)
solver.add(W < L)

# 2. Farley's lecture must be earlier than the oil paintings lecture.
solver.add(F < O)

# 3. Holden's lecture must be earlier than both Garcia's and Jiang's lectures.
solver.add(H < G)
solver.add(H < J)

# 4. The watercolors lecture is third.
solver.add(W == 3)

# Now evaluate each option

# Option A: Farley gives the watercolors lecture.
opt_a = (F == W)

# Option B: Garcia gives the oil paintings lecture.
opt_b = (G == O)

# Option C: Garcia gives the sculptures lecture.
opt_c = (G == S)

# Option D: Holden gives the sculptures lecture.
opt_d = (H == S)

# Option E: Jiang gives the lithographs lecture.
opt_e = (J == L)

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