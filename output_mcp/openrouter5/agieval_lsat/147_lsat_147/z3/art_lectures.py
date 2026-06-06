from z3 import *

solver = Solver()

# Four art historians: Farley, Garcia, Holden, Jiang
# Four topics: lithographs, oil paintings, sculptures, watercolors
# Each gives a lecture on a different topic, one at a time (positions 0-3, 0=earliest)

# We'll model positions (order) for each historian and each topic
# Positions are 0, 1, 2, 3 (0 = earliest, 3 = latest)

# Historian variables: the position (order) of each historian's lecture
F, G, H, J = Ints('F G H J')
# Topic variables: the position of each topic's lecture
L, O, S, W = Ints('L O S W')

# Domain constraints: all positions are 0..3
historian_vars = [F, G, H, J]
topic_vars = [L, O, S, W]
all_vars = historian_vars + topic_vars
for v in all_vars:
    solver.add(v >= 0, v <= 3)

# All historians have distinct positions
solver.add(Distinct(historian_vars))
# All topics have distinct positions
solver.add(Distinct(topic_vars))

# The historian giving a topic's lecture must be at the same position as that topic.
# So we need to link historians to topics. We can do this by saying:
# For each historian, the topic they give is at the same position.
# But we don't have a direct mapping variable. Instead, we can use the fact that
# the positions of historians and topics are both a permutation of 0..3.
# The constraint "Farley gives the lithographs lecture" means F == L.
# So we can encode the constraints using equality of positions.

# Constraint 1: The oil paintings lecture and the watercolors lecture must both be earlier than the lithographs lecture.
solver.add(O < L)
solver.add(W < L)

# Constraint 2: Farley's lecture must be earlier than the oil paintings lecture.
solver.add(F < O)

# Constraint 3: Holden's lecture must be earlier than both Garcia's lecture and Jiang's lecture.
solver.add(H < G)
solver.add(H < J)

# Now evaluate each option
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