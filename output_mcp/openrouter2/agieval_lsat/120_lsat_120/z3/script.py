from z3 import *
solver = Solver()
# declare Int variables for each band
slot_U = Int('slot_U')
slot_V = Int('slot_V')
slot_W = Int('slot_W')
slot_X = Int('slot_X')
slot_Y = Int('slot_Y')
slot_Z = Int('slot_Z')
# domain constraints
for s in [slot_U, slot_V, slot_W, slot_X, slot_Y, slot_Z]:
    solver.add(s >= 1, s <= 6)
# all distinct
solver.add(Distinct([slot_U, slot_V, slot_W, slot_X, slot_Y, slot_Z]))
# constraints
solver.add(slot_V < slot_Z)  # Vegemite earlier than Zircon
solver.add(slot_W < slot_X)  # Wellspring earlier than Xpert
solver.add(slot_Z < slot_X)  # Zircon earlier than Xpert
solver.add(slot_U >= 4)      # Uneasy in last three slots
solver.add(slot_Y <= 3)      # Yardsign in first three slots
# option constraints
opt_a_constr = (slot_Y == 1)
opt_b_constr = Or(slot_V == 1, slot_W == 1)
opt_c_constr = Or(slot_V == 1, slot_Y == 1)
opt_d_constr = Or(slot_V == 1, slot_W == 1, slot_Y == 1)
opt_e_constr = Or(slot_V == 1, slot_W == 1, slot_Y == 1, slot_Z == 1)
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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