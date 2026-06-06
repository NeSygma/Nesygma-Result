from z3 import *

# Declare variables
bands = ['Uneasy', 'Vegemite', 'Wellspring', 'Xpert', 'Yardsign', 'Zircon']
slot = {b: Int(f'slot_{b}') for b in bands}

solver = Solver()

# Base constraints
# All slots between 1 and 6
for b in bands:
    solver.add(slot[b] >= 1, slot[b] <= 6)

# All distinct
solver.add(Distinct([slot[b] for b in bands]))

# Constraint 1: Vegemite < Zircon
solver.add(slot['Vegemite'] < slot['Zircon'])

# Constraint 3: Uneasy in last three slots
solver.add(Or([slot['Uneasy'] == i for i in [4,5,6]]))

# Constraint 4: Yardsign in first three slots
solver.add(Or([slot['Yardsign'] == i for i in [1,2,3]]))

# Original constraint 2: Wellspring < Xpert and Zircon < Xpert
original_constr = And(slot['Wellspring'] < slot['Xpert'], slot['Zircon'] < slot['Xpert'])

# Now define alternatives
alternatives = {
    'A': And(slot['Vegemite'] < slot['Xpert'],
             slot['Wellspring'] < slot['Xpert'],
             slot['Yardsign'] < slot['Xpert'],
             slot['Zircon'] < slot['Xpert']),
    'B': And(slot['Vegemite'] < slot['Wellspring'],
             slot['Wellspring'] < slot['Zircon']),
    'C': And(slot['Vegemite'] < slot['Xpert'],
             slot['Wellspring'] < slot['Xpert']),
    'D': Or(slot['Xpert'] == slot['Uneasy'] + 1,
            slot['Xpert'] == slot['Uneasy'] - 1),
    'E': Or(slot['Xpert'] == 5,
            slot['Xpert'] == 6)
}

found_options = []
for letter, alt_constr in alternatives.items():
    # Check if base+original implies alt
    s1 = Solver()
    s1.add(solver.assertions())  # base constraints
    s1.add(original_constr)
    s1.add(Not(alt_constr))
    res1 = s1.check()
    
    # Check if base+alt implies original
    s2 = Solver()
    s2.add(solver.assertions())  # base constraints
    s2.add(alt_constr)
    s2.add(Not(original_constr))
    res2 = s2.check()
    
    if res1 == unsat and res2 == unsat:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")