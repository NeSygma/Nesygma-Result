from z3 import *

solver = Solver()

# Declare slot variables for each movie
h = Int('h')
m = Int('m')
r = Int('r')
s = Int('s')
w = Int('w')

# Domain constraints
solver.add(h >= 0, h <= 4)
solver.add(m >= 0, m <= 4)
solver.add(r >= 0, r <= 4)
solver.add(s >= 0, s <= 4)
solver.add(w >= 0, w <= 4)
solver.add(Distinct([h,m,r,s,w]))

# Helper functions
def screen_of(i):
    return If(i == 0, 1,
              If(i == 1, 1,
                 If(i == 2, 2,
                    If(i == 3, 2,
                       If(i == 4, 3, 0))))

def time_of(i):
    return If(i == 0, 0,
              If(i == 1, 2,
                 If(i == 2, 0,
                    If(i == 3, 2,
                       If(i == 4, 1, 0))))

# Base constraints
solver.add(s != 4)  # S not on screen3
solver.add(r != 2, r != 3)  # R not on screen2
solver.add(screen_of(h) != screen_of(m))  # H and M on different screens
solver.add(time_of(w) < time_of(h))  # W before H

# Define option constraints
opt_a_constr = [s == 2, h == 3]  # A: sci-fi at 7pm (slot2), horror at 9pm (slot3)
opt_b_constr = [s == 2, m == 3]  # B: sci-fi at 7pm, mystery at 9pm
opt_c_constr = [s == 2, w == 3]  # C: sci-fi at 7pm, western at 9pm
opt_d_constr = [w == 2, h == 3]  # D: western at 7pm, horror at 9pm
opt_e_constr = [w == 2, m == 3]  # E: western at 7pm, mystery at 9pm

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