from z3 import *

# Base constraints (shared for all options)
def get_base_constraints():
    solver = Solver()
    uneasy = Int('uneasy')
    vegemite = Int('vegemite')
    wellspring = Int('wellspring')
    xpert = Int('xpert')
    yardsign = Int('yardsign')
    zircon = Int('zircon')

    slots = [uneasy, vegemite, wellspring, xpert, yardsign, zircon]
    solver.add(Distinct(slots))
    for slot in slots:
        solver.add(slot >= 1, slot <= 6)

    # Constraints:
    # 1. Vegemite performs earlier than Zircon
    solver.add(vegemite < zircon)
    # 2. Wellspring and Zircon perform earlier than Xpert
    solver.add(wellspring < xpert)
    solver.add(zircon < xpert)
    # 3. Uneasy performs in one of the last three slots
    solver.add(Or(uneasy == 4, uneasy == 5, uneasy == 6))
    # 4. Yardsign performs in one of the first three slots
    solver.add(Or(yardsign == 1, yardsign == 2, yardsign == 3))
    
    return solver, {
        'uneasy': uneasy,
        'vegemite': vegemite,
        'wellspring': wellspring,
        'xpert': xpert,
        'yardsign': yardsign,
        'zircon': zircon
    }

# Evaluate each option independently
found_options = []

# Option A: Yardsign
solver, vars = get_base_constraints()
solver.add(vars['yardsign'] == 1)
if solver.check() == sat:
    found_options.append("A")

# Option B: Vegemite, Wellspring
solver, vars = get_base_constraints()
solver.add(Or(vars['vegemite'] == 1, vars['wellspring'] == 1))
if solver.check() == sat:
    found_options.append("B")

# Option C: Vegemite, Yardsign
solver, vars = get_base_constraints()
solver.add(Or(vars['vegemite'] == 1, vars['yardsign'] == 1))
if solver.check() == sat:
    found_options.append("C")

# Option D: Vegemite, Wellspring, Yardsign
solver, vars = get_base_constraints()
solver.add(Or(vars['vegemite'] == 1, vars['wellspring'] == 1, vars['yardsign'] == 1))
if solver.check() == sat:
    found_options.append("D")

# Option E: Vegemite, Wellspring, Yardsign, Zircon
solver, vars = get_base_constraints()
solver.add(Or(vars['vegemite'] == 1, vars['wellspring'] == 1, vars['yardsign'] == 1, vars['zircon'] == 1))
if solver.check() == sat:
    found_options.append("E")

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")