from z3 import *
solver = Solver()

# Declare position variables
f = Int('f')
g = Int('g')
h = Int('h')
j = Int('j')

# Map lecturer initials to variables
var_map = {'f': f, 'g': g, 'h': h, 'j': j}

# Define position mappings for each option
pos_A = {'f': 1, 'h': 2, 'g': 3, 'j': 4}
oil_lecturer_A = 'g'
water_lecturer_A = 'j'
lith_lecturer_A = 'h'

pos_B = {'f': 1, 'j': 2, 'h': 3, 'g': 4}
oil_lecturer_B = 'j'
water_lecturer_B = 'f'
lith_lecturer_B = 'g'

pos_C = {'g': 1, 'f': 2, 'h': 3, 'j': 4}
oil_lecturer_C = 'h'
water_lecturer_C = 'f'
lith_lecturer_C = 'j'

pos_D = {'h': 1, 'j': 2, 'f': 3, 'g': 4}
oil_lecturer_D = 'h'
water_lecturer_D = 'j'
lith_lecturer_D = 'f'

pos_E = {'h': 1, 'f': 2, 'j': 3, 'g': 4}
oil_lecturer_E = 'j'
water_lecturer_E = 'f'
lith_lecturer_E = 'g'

# Helper function to build constraint for an option
def build_constraint(pos, oil_lecturer, water_lecturer, lith_lecturer):
    oil_pos = var_map[oil_lecturer]
    water_pos = var_map[water_lecturer]
    lith_pos = var_map[lith_lecturer]
    return And(
        Distinct(f, g, h, j),
        f == pos['f'],
        g == pos['g'],
        h == pos['h'],
        j == pos['j'],
        oil_pos < lith_pos,
        water_pos < lith_pos,
        f < oil_pos,
        h < g,
        h < j
    )

# Build constraints for each option
opt_a_constr = build_constraint(pos_A, oil_lecturer_A, water_lecturer_A, lith_lecturer_A)
opt_b_constr = build_constraint(pos_B, oil_lecturer_B, water_lecturer_B, lith_lecturer_B)
opt_c_constr = build_constraint(pos_C, oil_lecturer_C, water_lecturer_C, lith_lecturer_C)
opt_d_constr = build_constraint(pos_D, oil_lecturer_D, water_lecturer_D, lith_lecturer_D)
opt_e_constr = build_constraint(pos_E, oil_lecturer_E, water_lecturer_E, lith_lecturer_E)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output result according to skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")