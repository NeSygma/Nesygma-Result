from z3 import *

# Historians: Farley (F), Garcia (G), Holden (H), Jiang (J)
# Topics: Lithographs (L), Oil paintings (O), Sculptures (S), Watercolors (W)
# Time slots: 1, 2, 3, 4

# Variables
h_f, h_g, h_h, h_j = Ints('h_f h_g h_h h_j')
t_l, t_o, t_s, t_w = Ints('t_l t_o t_s t_w')

solver = Solver()

# Domain constraints
for var in [h_f, h_g, h_h, h_j, t_l, t_o, t_s, t_w]:
    solver.add(var >= 1, var <= 4)

solver.add(Distinct(h_f, h_g, h_h, h_j))
solver.add(Distinct(t_l, t_o, t_s, t_w))

# Constraints
# 1. The oil paintings lecture and the watercolors lecture must both be earlier than the lithographs lecture.
solver.add(t_o < t_l)
solver.add(t_w < t_l)

# 2. Farley's lecture must be earlier than the oil paintings lecture.
solver.add(h_f < t_o)

# 3. Holden's lecture must be earlier than both Garcia's lecture and Jiang's lecture.
solver.add(h_h < h_g)
solver.add(h_h < h_j)

# Options
options = [
    ("A", h_f < t_s),
    ("B", h_h < t_l),
    ("C", t_s < h_g),
    ("D", t_s < h_j),
    ("E", t_w < h_g)
]

# Check which option must be true (i.e., its negation is unsat)
valid_options = []
for letter, constr in options:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        valid_options.append(letter)
    solver.pop()

if len(valid_options) == 1:
    print("STATUS: sat")
    print(f"answer:{valid_options[0]}")
elif len(valid_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {valid_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")