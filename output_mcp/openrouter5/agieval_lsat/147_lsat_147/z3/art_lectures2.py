from z3 import *

solver = Solver()

# Four art historians: Farley, Garcia, Holden, Jiang
# Four topics: lithographs, oil paintings, sculptures, watercolors
# Each gives a lecture on a different topic, one at a time (positions 0-3, 0=earliest)

# We need to model both the order of historians and which topic each gives.
# Let's use two sets of variables:
# historian_order[i] = which historian is in position i (0..3)
# topic_order[i] = which topic is in position i (0..3)
# Or better: assign each historian a position and each topic a position,
# and link them via the constraint that the historian giving a topic is at the same position.

# Actually, let's use a different approach: assign each historian a topic.
# topic_of[historian] = topic index (0=L, 1=O, 2=S, 3=W)
# position_of[historian] = position (0..3)

F, G, H, J = Ints('F G H J')  # positions of historians
L_t, O_t, S_t, W_t = Ints('L_t O_t S_t W_t')  # positions of topics

# Domain
for v in [F, G, H, J, L_t, O_t, S_t, W_t]:
    solver.add(v >= 0, v <= 3)

# All distinct
solver.add(Distinct(F, G, H, J))
solver.add(Distinct(L_t, O_t, S_t, W_t))

# Constraints
solver.add(O_t < L_t)
solver.add(W_t < L_t)
solver.add(F < O_t)
solver.add(H < G)
solver.add(H < J)

# Now for each option, we need to encode "X gives topic Y"
# X gives topic Y means position_of_X == position_of_topic_Y
# Option A: Farley gives lithographs => F == L_t
opt_a = (F == L_t)

# Option B: Garcia gives sculptures => G == S_t
opt_b = (G == S_t)

# Option C: Garcia gives watercolors => G == W_t
opt_c = (G == W_t)

# Option D: Holden gives oil paintings => H == O_t
opt_d = (H == O_t)

# Option E: Jiang gives watercolors => J == W_t
opt_e = (J == W_t)

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