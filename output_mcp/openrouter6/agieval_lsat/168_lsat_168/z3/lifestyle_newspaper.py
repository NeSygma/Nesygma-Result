from z3 import *

solver = Solver()

# Declare variables for counts per photographer per section
L_f, L_g, L_h = Ints('L_f L_g L_h')
M_f, M_g, M_h = Ints('M_f M_g M_h')
S_f, S_g, S_h = Ints('S_f S_g S_h')

# Base constraints
# Each section has exactly two photos
solver.add(L_f + L_g + L_h == 2)
solver.add(M_f + M_g + M_h == 2)
solver.add(S_f + S_g + S_h == 2)

# Each photographer total between 1 and 3
T_f = L_f + M_f + S_f
T_g = L_g + M_g + S_g
T_h = L_h + M_h + S_h
solver.add(T_f >= 1, T_f <= 3)
solver.add(T_g >= 1, T_g <= 3)
solver.add(T_h >= 1, T_h <= 3)

# At least one photo in Lifestyle by a photographer who also has at least one in Metro
solver.add(Or(
    And(L_f > 0, M_f > 0),
    And(L_g > 0, M_g > 0),
    And(L_h > 0, M_h > 0)
))

# Hue's photographs in Lifestyle equals Fuentes photographs in Sports
solver.add(L_h == S_f)

# No Gagnon in Sports
solver.add(S_g == 0)

# Non-negativity (already implied by sums and bounds, but explicit)
solver.add(L_f >= 0, L_g >= 0, L_h >= 0)
solver.add(M_f >= 0, M_g >= 0, M_h >= 0)
solver.add(S_f >= 0, S_g >= 0, S_h >= 0)

# Define option constraints
opt_a_constr = [
    L_f == 2, L_g == 0, L_h == 0,
    M_f == 1, M_g == 0, M_h == 1,
    S_f == 0, S_g == 1, S_h == 1
]

opt_b_constr = [
    L_f == 1, L_g == 1, L_h == 0,
    M_f == 1, M_g == 1, M_h == 0,
    S_f == 0, S_g == 0, S_h == 2
]

opt_c_constr = [
    L_f == 2, L_g == 0, L_h == 0,
    M_f == 0, M_g == 2, M_h == 0,
    S_f == 0, S_g == 0, S_h == 2
]

opt_d_constr = [
    L_f == 0, L_g == 2, L_h == 0,
    M_f == 1, M_g == 1, M_h == 0,
    S_f == 1, S_g == 0, S_h == 1
]

opt_e_constr = [
    L_f == 0, L_g == 1, L_h == 1,
    M_f == 0, M_g == 0, M_h == 2,
    S_f == 1, S_g == 0, S_h == 1
]

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