from z3 import *

# Base constraints (excluding Wellspring and Zircon < Xpert)
# These are the constraints that are always present, regardless of the option.

def get_base_constraints():
    solver = Solver()
    uneasy = Int('uneasy')
    vegemite = Int('vegemite')
    wellspring = Int('wellspring')
    xpert = Int('xpert')
    yardsign = Int('yardsign')
    zircon = Int('zircon')

    # All slots are between 1 and 6
    solver.add(uneasy >= 1, uneasy <= 6)
    solver.add(vegemite >= 1, vegemite <= 6)
    solver.add(wellspring >= 1, wellspring <= 6)
    solver.add(xpert >= 1, xpert <= 6)
    solver.add(yardsign >= 1, yardsign <= 6)
    solver.add(zircon >= 1, zircon <= 6)

    # All bands are in distinct slots
    disjoint = [uneasy != vegemite, uneasy != wellspring, uneasy != xpert, uneasy != yardsign, uneasy != zircon,
                vegemite != wellspring, vegemite != xpert, vegemite != yardsign, vegemite != zircon,
                wellspring != xpert, wellspring != yardsign, wellspring != zircon,
                xpert != yardsign, xpert != zircon,
                yardsign != zircon]
    solver.add(And(disjoint))

    # Vegemite performs in an earlier slot than Zircon
    solver.add(vegemite < zircon)

    # Uneasy performs in one of the last three slots (4, 5, or 6)
    solver.add(Or(uneasy == 4, uneasy == 5, uneasy == 6))

    # Yardsign performs in one of the first three slots (1, 2, or 3)
    solver.add(Or(yardsign == 1, yardsign == 2, yardsign == 3))

    return solver, {
        'uneasy': uneasy,
        'vegemite': vegemite,
        'wellspring': wellspring,
        'xpert': xpert,
        'yardsign': yardsign,
        'zircon': zircon
    }

# Get the base solver and variables
base_solver, vars_dict = get_base_constraints()
uneasy, vegemite, wellspring, xpert, yardsign, zircon = vars_dict.values()

# Original constraint: Wellspring and Zircon each perform in an earlier slot than Xpert
original_constraint = And(wellspring < xpert, zircon < xpert)

# Enumerate all models under the original constraint
original_models = []
base_solver.push()
base_solver.add(original_constraint)
while base_solver.check() == sat:
    m = base_solver.model()
    model_dict = {
        'uneasy': m[uneasy].as_long(),
        'vegemite': m[vegemite].as_long(),
        'wellspring': m[wellspring].as_long(),
        'xpert': m[xpert].as_long(),
        'yardsign': m[yardsign].as_long(),
        'zircon': m[zircon].as_long()
    }
    original_models.append(model_dict)
    base_solver.add(Or(
        uneasy != m[uneasy],
        vegemite != m[vegemite],
        wellspring != m[wellspring],
        xpert != m[xpert],
        yardsign != m[yardsign],
        zircon != m[zircon]
    ))
base_solver.pop()

# Now, evaluate each option to see which one produces the same set of models
found_options = []

# Option A: Only Uneasy can perform in a later slot than Xpert.
# Interpretation: Xpert must be in slot 4,5, or 6. Uneasy must be in slot 5 or 6, and Uneasy > Xpert.
# All other bands must be <= Xpert (but since all slots are distinct, they must be < Xpert).
option_a_solver, option_a_vars = get_base_constraints()
option_a_uneasy, option_a_vegemite, option_a_wellspring, option_a_xpert, option_a_yardsign, option_a_zircon = option_a_vars.values()

option_a_solver.add(Or(option_a_xpert == 4, option_a_xpert == 5, option_a_xpert == 6))
option_a_solver.add(Or(option_a_uneasy == 5, option_a_uneasy == 6))
option_a_solver.add(option_a_uneasy > option_a_xpert)
option_a_solver.add(option_a_wellspring < option_a_xpert)
option_a_solver.add(option_a_vegemite < option_a_xpert)
option_a_solver.add(option_a_yardsign < option_a_xpert)
option_a_solver.add(option_a_zircon < option_a_xpert)

option_a_models = []
while option_a_solver.check() == sat:
    m = option_a_solver.model()
    model_dict = {
        'uneasy': m[option_a_uneasy].as_long(),
        'vegemite': m[option_a_vegemite].as_long(),
        'wellspring': m[option_a_wellspring].as_long(),
        'xpert': m[option_a_xpert].as_long(),
        'yardsign': m[option_a_yardsign].as_long(),
        'zircon': m[option_a_zircon].as_long()
    }
    option_a_models.append(model_dict)
    option_a_solver.add(Or(
        option_a_uneasy != m[option_a_uneasy],
        option_a_vegemite != m[option_a_vegemite],
        option_a_wellspring != m[option_a_wellspring],
        option_a_xpert != m[option_a_xpert],
        option_a_yardsign != m[option_a_yardsign],
        option_a_zircon != m[option_a_zircon]
    ))

if option_a_models == original_models:
    found_options.append("A")

# Option B: Vegemite performs in an earlier slot than Wellspring, which performs in an earlier slot than Zircon.
option_b_solver, option_b_vars = get_base_constraints()
option_b_uneasy, option_b_vegemite, option_b_wellspring, option_b_xpert, option_b_yardsign, option_b_zircon = option_b_vars.values()

option_b_solver.add(option_b_vegemite < option_b_wellspring)
option_b_solver.add(option_b_wellspring < option_b_zircon)

option_b_models = []
while option_b_solver.check() == sat:
    m = option_b_solver.model()
    model_dict = {
        'uneasy': m[option_b_uneasy].as_long(),
        'vegemite': m[option_b_vegemite].as_long(),
        'wellspring': m[option_b_wellspring].as_long(),
        'xpert': m[option_b_xpert].as_long(),
        'yardsign': m[option_b_yardsign].as_long(),
        'zircon': m[option_b_zircon].as_long()
    }
    option_b_models.append(model_dict)
    option_b_solver.add(Or(
        option_b_uneasy != m[option_b_uneasy],
        option_b_vegemite != m[option_b_vegemite],
        option_b_wellspring != m[option_b_wellspring],
        option_b_xpert != m[option_b_xpert],
        option_b_yardsign != m[option_b_yardsign],
        option_b_zircon != m[option_b_zircon]
    ))

if option_b_models == original_models:
    found_options.append("B")

# Option C: Vegemite and Wellspring each perform in an earlier slot than Xpert.
option_c_solver, option_c_vars = get_base_constraints()
option_c_uneasy, option_c_vegemite, option_c_wellspring, option_c_xpert, option_c_yardsign, option_c_zircon = option_c_vars.values()

option_c_solver.add(option_c_vegemite < option_c_xpert)
option_c_solver.add(option_c_wellspring < option_c_xpert)

option_c_models = []
while option_c_solver.check() == sat:
    m = option_c_solver.model()
    model_dict = {
        'uneasy': m[option_c_uneasy].as_long(),
        'vegemite': m[option_c_vegemite].as_long(),
        'wellspring': m[option_c_wellspring].as_long(),
        'xpert': m[option_c_xpert].as_long(),
        'yardsign': m[option_c_yardsign].as_long(),
        'zircon': m[option_c_zircon].as_long()
    }
    option_c_models.append(model_dict)
    option_c_solver.add(Or(
        option_c_uneasy != m[option_c_uneasy],
        option_c_vegemite != m[option_c_vegemite],
        option_c_wellspring != m[option_c_wellspring],
        option_c_xpert != m[option_c_xpert],
        option_c_yardsign != m[option_c_yardsign],
        option_c_zircon != m[option_c_zircon]
    ))

if option_c_models == original_models:
    found_options.append("C")

# Option D: Xpert performs either immediately before or immediately after Uneasy.
option_d_solver, option_d_vars = get_base_constraints()
option_d_uneasy, option_d_vegemite, option_d_wellspring, option_d_xpert, option_d_yardsign, option_d_zircon = option_d_vars.values()

option_d_solver.add(Or(option_d_xpert == option_d_uneasy - 1, option_d_xpert == option_d_uneasy + 1))

option_d_models = []
while option_d_solver.check() == sat:
    m = option_d_solver.model()
    model_dict = {
        'uneasy': m[option_d_uneasy].as_long(),
        'vegemite': m[option_d_vegemite].as_long(),
        'wellspring': m[option_d_wellspring].as_long(),
        'xpert': m[option_d_xpert].as_long(),
        'yardsign': m[option_d_yardsign].as_long(),
        'zircon': m[option_d_zircon].as_long()
    }
    option_d_models.append(model_dict)
    option_d_solver.add(Or(
        option_d_uneasy != m[option_d_uneasy],
        option_d_vegemite != m[option_d_vegemite],
        option_d_wellspring != m[option_d_wellspring],
        option_d_xpert != m[option_d_xpert],
        option_d_yardsign != m[option_d_yardsign],
        option_d_zircon != m[option_d_zircon]
    ))

if option_d_models == original_models:
    found_options.append("D")

# Option E: Xpert performs in either slot five or slot six.
option_e_solver, option_e_vars = get_base_constraints()
option_e_uneasy, option_e_vegemite, option_e_wellspring, option_e_xpert, option_e_yardsign, option_e_zircon = option_e_vars.values()

option_e_solver.add(Or(option_e_xpert == 5, option_e_xpert == 6))

option_e_models = []
while option_e_solver.check() == sat:
    m = option_e_solver.model()
    model_dict = {
        'uneasy': m[option_e_uneasy].as_long(),
        'vegemite': m[option_e_vegemite].as_long(),
        'wellspring': m[option_e_wellspring].as_long(),
        'xpert': m[option_e_xpert].as_long(),
        'yardsign': m[option_e_yardsign].as_long(),
        'zircon': m[option_e_zircon].as_long()
    }
    option_e_models.append(model_dict)
    option_e_solver.add(Or(
        option_e_uneasy != m[option_e_uneasy],
        option_e_vegemite != m[option_e_vegemite],
        option_e_wellspring != m[option_e_wellspring],
        option_e_xpert != m[option_e_xpert],
        option_e_yardsign != m[option_e_yardsign],
        option_e_zircon != m[option_e_zircon]
    ))

if option_e_models == original_models:
    found_options.append("E")

# Now, determine the result based on found_options
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")