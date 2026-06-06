from z3 import *

solver = Solver()

# We have 4 positions (0=earliest, 3=latest).
# Each position has a historian and a topic.
# Let's use a different encoding: assign each historian a position, each topic a position.

# Positions for historians
F, G, H, J = Ints('F G H J')
# Positions for topics
L, O, S, W = Ints('L O S W')

# Domain: 0 to 3
for var in [F, G, H, J, L, O, S, W]:
    solver.add(var >= 0, var <= 3)

# All different for historians
solver.add(Distinct(F, G, H, J))
# All different for topics
solver.add(Distinct(L, O, S, W))

# Constraints:
# Oil paintings (O) and watercolors (W) must both be earlier than lithographs (L)
solver.add(O < L)
solver.add(W < L)

# Farley's lecture must be earlier than the oil paintings lecture
solver.add(F < O)

# Holden's lecture must be earlier than both Garcia's and Jiang's
solver.add(H < G)
solver.add(H < J)

# Now evaluate options
# Option A: Farley gives the lithographs lecture => F == L
opt_a = (F == L)

# Option B: Garcia gives the sculptures lecture => G == S
opt_b = (G == S)

# Option C: Garcia gives the watercolors lecture => G == W
opt_c = (G == W)

# Option D: Holden gives the oil paintings lecture => H == O
opt_d = (H == O)

# Option E: Jiang gives the watercolors lecture => J == W
opt_e = (J == W)

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