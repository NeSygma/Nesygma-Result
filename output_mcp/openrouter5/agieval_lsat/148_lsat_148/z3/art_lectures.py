from z3 import *

# Four art historians: Farley, Garcia, Holden, Jiang
# Four topics: lithographs, oil paintings, sculptures, watercolors
# Each gives a lecture on a different topic, one at a time (positions 1-4)

# We'll model positions 1,2,3,4 for each historian and each topic.
# Let's use Int variables for positions of historians and topics.

# Historians
F, G, H, J = Ints('F G H J')
# Topics
L, O, S, W = Ints('L O S W')  # lithographs, oil paintings, sculptures, watercolors

solver = Solver()

# Domain: positions 1 to 4
historians = [F, G, H, J]
topics = [L, O, S, W]
all_vars = historians + topics

for v in all_vars:
    solver.add(v >= 1, v <= 4)

# All different positions for historians
solver.add(Distinct(historians))
# All different positions for topics
solver.add(Distinct(topics))

# Constraints:
# 1. Oil paintings (O) and watercolors (W) must both be earlier than lithographs (L)
solver.add(O < L)
solver.add(W < L)

# 2. Farley's lecture must be earlier than the oil paintings lecture
solver.add(F < O)

# 3. Holden's lecture must be earlier than both Garcia's and Jiang's lectures
solver.add(H < G)
solver.add(H < J)

# Additional condition: Garcia gives the sculptures lecture
# So Garcia's position = sculptures position
solver.add(G == S)

# Now evaluate each option
# Option A: The lithographs lecture is third -> L == 3
opt_a = (L == 3)

# Option B: The oil paintings lecture is third -> O == 3
opt_b = (O == 3)

# Option C: The sculptures lecture is first -> S == 1
opt_c = (S == 1)

# Option D: The sculptures lecture is second -> S == 2
opt_d = (S == 2)

# Option E: The watercolors lecture is second -> W == 2
opt_e = (W == 2)

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