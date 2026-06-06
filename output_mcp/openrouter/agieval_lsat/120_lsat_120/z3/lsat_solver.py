from z3 import *

def base_solver():
    # Bands indices
    bands = ['Uneasy', 'Vegemite', 'Wellspring', 'Xpert', 'Yardsign', 'Zircon']
    # Create Int variable for each band representing its slot (1..6)
    slot = {b: Int(f'slot_{b}') for b in bands}
    s = Solver()
    # Domain constraints
    for b in bands:
        s.add(slot[b] >= 1, slot[b] <= 6)
    # All different
    s.add(Distinct([slot[b] for b in bands]))
    # Constraints from problem
    # Vegemite earlier than Zircon
    s.add(slot['Vegemite'] < slot['Zircon'])
    # Wellspring earlier than Xpert
    s.add(slot['Wellspring'] < slot['Xpert'])
    # Zircon earlier than Xpert
    s.add(slot['Zircon'] < slot['Xpert'])
    # Uneasy in last three slots (4,5,6)
    s.add(slot['Uneasy'] >= 4)
    # Yardsign in first three slots (1,2,3)
    s.add(slot['Yardsign'] <= 3)
    return s, slot

# Compute possible bands for slot 1
s, slot = base_solver()
possible = set()
while s.check() == sat:
    m = s.model()
    # Find which band has slot == 1
    for b, var in slot.items():
        if m.eval(var).as_long() == 1:
            possible.add(b)
            break
    # Block this model
    block = []
    for var in slot.values():
        block.append(var != m.eval(var))
    s.add(Or(block))

# Define answer options
options = {
    'A': ['Yardsign'],
    'B': ['Vegemite', 'Wellspring'],
    'C': ['Vegemite', 'Yardsign'],
    'D': ['Vegemite', 'Wellspring', 'Yardsign'],
    'E': ['Vegemite', 'Wellspring', 'Yardsign', 'Zircon']
}

found_options = []
for letter, opt_list in options.items():
    # Create a fresh solver with base constraints
    s_opt, _ = base_solver()
    # Condition: possible set equals option set
    cond = BoolVal(set(possible) == set(opt_list))
    s_opt.add(cond)
    if s_opt.check() == sat:
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