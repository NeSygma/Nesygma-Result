from z3 import *

# Historians: F=0, G=1, H=2, J=3
F, G, H, J = 0, 1, 2, 3
# Topics: L=0, O=1, S=2, W=3
L, O, S, W = 0, 1, 2, 3

solver = Solver()

# slot_hist[i] = historian giving lecture in slot i (0=first, 1=second, 2=third, 3=fourth)
# slot_topic[i] = topic of the lecture in slot i
slot_hist = [Int(f'slot_hist_{i}') for i in range(4)]
slot_topic = [Int(f'slot_topic_{i}') for i in range(4)]

for i in range(4):
    solver.add(slot_hist[i] >= 0, slot_hist[i] <= 3)
    solver.add(slot_topic[i] >= 0, slot_topic[i] <= 3)

solver.add(Distinct(slot_hist))
solver.add(Distinct(slot_topic))

# Constraint 1: Oil paintings (O) and watercolors (W) must both be earlier than lithographs (L).
oil_before_litho = False
water_before_litho = False
for i in range(4):
    for j in range(4):
        if i < j:
            oil_before_litho = Or(oil_before_litho, And(slot_topic[i] == O, slot_topic[j] == L))
            water_before_litho = Or(water_before_litho, And(slot_topic[i] == W, slot_topic[j] == L))
solver.add(oil_before_litho)
solver.add(water_before_litho)

# Constraint 2: Farley's lecture must be earlier than the oil paintings lecture.
farley_before_oil = False
for i in range(4):
    for j in range(4):
        if i < j:
            farley_before_oil = Or(farley_before_oil, And(slot_hist[i] == F, slot_topic[j] == O))
solver.add(farley_before_oil)

# Constraint 3: Holden's lecture must be earlier than both Garcia's and Jiang's.
holden_before_garcia = False
holden_before_jiang = False
for i in range(4):
    for j in range(4):
        if i < j:
            holden_before_garcia = Or(holden_before_garcia, And(slot_hist[i] == H, slot_hist[j] == G))
            holden_before_jiang = Or(holden_before_jiang, And(slot_hist[i] == H, slot_hist[j] == J))
solver.add(holden_before_garcia)
solver.add(holden_before_jiang)

# Given: Garcia gives the sculptures lecture.
garcia_sculptures = False
for i in range(4):
    garcia_sculptures = Or(garcia_sculptures, And(slot_hist[i] == G, slot_topic[i] == S))
solver.add(garcia_sculptures)

# Options
# (A) The lithographs lecture is third.  (index 2)
opt_a = (slot_topic[2] == L)
# (B) The oil paintings lecture is third. (index 2)
opt_b = (slot_topic[2] == O)
# (C) The sculptures lecture is first. (index 0)
opt_c = (slot_topic[0] == S)
# (D) The sculptures lecture is second. (index 1)
opt_d = (slot_topic[1] == S)
# (E) The watercolors lecture is second. (index 1)
opt_e = (slot_topic[1] == W)

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