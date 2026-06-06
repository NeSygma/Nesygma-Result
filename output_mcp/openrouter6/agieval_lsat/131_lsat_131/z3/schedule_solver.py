from z3 import *

# Base constraints
solver = Solver()

# Slot numbers: 1: screen1-7, 2: screen1-9, 3: screen2-7, 4: screen2-9, 5: screen3-8
horror = Int('horror')
mystery = Int('mystery')
romance = Int('romance')
scifi = Int('scifi')
western = Int('western')

# All slots between 1 and 5
solver.add(horror >= 1, horror <= 5)
solver.add(mystery >= 1, mystery <= 5)
solver.add(romance >= 1, romance <= 5)
solver.add(scifi >= 1, scifi <= 5)
solver.add(western >= 1, western <= 5)

# All distinct
solver.add(Distinct([horror, mystery, romance, scifi, western]))

# Helper functions for screen and time
def get_screen(s):
    return If(Or(s == 1, s == 2), 1,
              If(Or(s == 3, s == 4), 2, 3))

def get_time(s):
    return If(Or(s == 1, s == 3), 7,
              If(Or(s == 2, s == 4), 9, 8))

# Constraint 1: Western before horror
solver.add(get_time(western) < get_time(horror))

# Constraint 2: Sci-fi not on screen 3
solver.add(get_screen(scifi) != 3)

# Constraint 3: Romance not on screen 2
solver.add(get_screen(romance) != 2)

# Constraint 4: Horror and mystery on different screens
solver.add(get_screen(horror) != get_screen(mystery))

# Additional condition: Romance before western
solver.add(get_time(romance) < get_time(western))

# Now define option constraints
opt_a_constr = (get_screen(horror) == 1)
opt_b_constr = (get_time(mystery) == 7)
opt_c_constr = (get_screen(mystery) == 2)
opt_d_constr = (get_time(scifi) == 9)
opt_e_constr = (get_screen(scifi) == 2)

# Evaluate each option using the skeleton
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