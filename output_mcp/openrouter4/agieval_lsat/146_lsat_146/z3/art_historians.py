from z3 import *

solver = Solver()

# Historians: Farley=0, Garcia=1, Holden=2, Jiang=3
F, G, H, J = 0, 1, 2, 3
hist_names = ["Farley", "Garcia", "Holden", "Jiang"]

# Topics: Lithographs=0, OilPaintings=1, Sculptures=2, Watercolors=3
L, O, S, W = 0, 1, 2, 3
topic_names = ["Lithographs", "OilPaintings", "Sculptures", "Watercolors"]

# Position of each historian's lecture (1-4)
hist_pos = [Int(f'hist_pos_{i}') for i in range(4)]
for i in range(4):
    solver.add(hist_pos[i] >= 1, hist_pos[i] <= 4)

# Position of each topic (1-4)
topic_pos = [Int(f'topic_pos_{i}') for i in range(4)]
for i in range(4):
    solver.add(topic_pos[i] >= 1, topic_pos[i] <= 4)

# All historian positions are distinct
solver.add(Distinct(hist_pos))

# All topic positions are distinct
solver.add(Distinct(topic_pos))

# Constraints:

# 1. Oil paintings and watercolors must both be earlier than lithographs
solver.add(topic_pos[O] < topic_pos[L])
solver.add(topic_pos[W] < topic_pos[L])

# 2. Farley's lecture must be earlier than the oil paintings lecture
solver.add(hist_pos[F] < topic_pos[O])

# 3. Holden's lecture must be earlier than both Garcia's and Jiang's
solver.add(hist_pos[H] < hist_pos[G])
solver.add(hist_pos[H] < hist_pos[J])

# Additional: The watercolors lecture is third
solver.add(topic_pos[W] == 3)

# Now evaluate each option
# Each option is: historian X gives topic Y => hist_pos[X] == topic_pos[Y]

options = []

# (A) Farley gives the watercolors lecture
opt_a = (hist_pos[F] == topic_pos[W])

# (B) Garcia gives the oil paintings lecture
opt_b = (hist_pos[G] == topic_pos[O])

# (C) Garcia gives the sculptures lecture
opt_c = (hist_pos[G] == topic_pos[S])

# (D) Holden gives the sculptures lecture
opt_d = (hist_pos[H] == topic_pos[S])

# (E) Jiang gives the lithographs lecture
opt_e = (hist_pos[J] == topic_pos[L])

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