from z3 import *

# Slot numbers: 1: screen1-7, 2: screen1-9, 3: screen2-7, 4: screen2-9, 5: screen3-8
horror = Int('horror')
mystery = Int('mystery')
romance = Int('romance')
scifi = Int('scifi')
western = Int('western')

solver = Solver()
solver.add(horror >= 1, horror <= 5)
solver.add(mystery >= 1, mystery <= 5)
solver.add(romance >= 1, romance <= 5)
solver.add(scifi >= 1, scifi <= 5)
solver.add(western >= 1, western <= 5)
solver.add(Distinct([horror, mystery, romance, scifi, western]))

def get_screen(s):
    return If(Or(s == 1, s == 2), 1,
              If(Or(s == 3, s == 4), 2, 3))

def get_time(s):
    return If(Or(s == 1, s == 3), 7,
              If(Or(s == 2, s == 4), 9, 8))

# Base constraints
solver.add(get_time(western) < get_time(horror))
solver.add(get_screen(scifi) != 3)
solver.add(get_screen(romance) != 2)
solver.add(get_screen(horror) != get_screen(mystery))
# Additional condition: romance before western
solver.add(get_time(romance) < get_time(western))

# Define option constraints (negations)
opt_a_constr = Not(get_screen(horror) == 1)  # horror not on screen 1
opt_b_constr = Not(Or(mystery == 1, mystery == 3))  # mystery not at 7 PM
opt_c_constr = Not(Or(mystery == 3, mystery == 4))  # mystery not on screen 2
opt_d_constr = Not(Or(scifi == 2, scifi == 4))  # sci-fi not at 9 PM
opt_e_constr = Not(Or(scifi == 3, scifi == 4))  # sci-fi not on screen 2

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:  # negation leads to unsat => option must be true
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