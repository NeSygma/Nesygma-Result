from z3 import *

# Define movie IDs
movies = ['H', 'M', 'R', 'S', 'W']
slot = {m: Int(f'slot_{m}') for m in movies}

# Slot to screen and time mapping
def screen_of(slot_val):
    # slot_val is an integer expression
    return If(Or(slot_val == 0, slot_val == 1), 1,
              If(Or(slot_val == 2, slot_val == 3), 2, 3))

def time_of(slot_val):
    return If(Or(slot_val == 0, slot_val == 2), 7,
              If(Or(slot_val == 1, slot_val == 3), 9, 8))

solver = Solver()

# Domain constraints: each slot between 0 and 4
for m in movies:
    solver.add(slot[m] >= 0, slot[m] <= 4)

# All slots distinct
solver.add(Distinct([slot[m] for m in movies]))

# Base constraints
# 1. Western before horror: time(W) < time(H)
solver.add(time_of(slot['W']) < time_of(slot['H']))
# 2. Sci-fi not on screen 3: screen(S) != 3 => slot[S] != 4
solver.add(slot['S'] != 4)
# 3. Romance not on screen 2: screen(R) != 2 => slot[R] not in {2,3}
solver.add(Or(slot['R'] != 2, slot['R'] != 3))  # Actually need slot[R] not in {2,3}
# Better: slot[R] != 2 and slot[R] != 3
solver.add(slot['R'] != 2)
solver.add(slot['R'] != 3)
# 4. Horror and mystery different screens: screen(H) != screen(M)
solver.add(screen_of(slot['H']) != screen_of(slot['M']))

# Options for screen 1: slot 0 (7 PM) and slot 1 (9 PM)
# Option A: sci-fi, horror
opt_a_constr = And(slot['S'] == 0, slot['H'] == 1)
# Option B: sci-fi, mystery
opt_b_constr = And(slot['S'] == 0, slot['M'] == 1)
# Option C: western, horror
opt_c_constr = And(slot['W'] == 0, slot['H'] == 1)
# Option D: western, mystery
opt_d_constr = And(slot['W'] == 0, slot['M'] == 1)
# Option E: western, sci-fi
opt_e_constr = And(slot['W'] == 0, slot['S'] == 1)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:  # We are looking for impossible options
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