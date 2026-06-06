from z3 import *

# Declare the positions of each band member
pos = {
    'guitarist': Int('guitarist'),
    'keyboard': Int('keyboard'),
    'percussionist': Int('percussionist'),
    'saxophonist': Int('saxophonist'),
    'trumpeter': Int('trumpeter'),
    'violinist': Int('violinist')
}

# Create a solver
solver = Solver()

# Add constraints
solver.add(Distinct(list(pos.values())))  # Each position is unique
solver.add(pos['guitarist'] != 4)  # Guitarist does not perform the fourth solo
solver.add(pos['percussionist'] < pos['keyboard'])  # Percussionist before keyboard
solver.add(pos['violinist'] < pos['keyboard'])  # Violinist before keyboard
solver.add(pos['keyboard'] < pos['guitarist'])  # Keyboard before guitarist

# Saxophonist performs after exactly one of percussionist or trumpeter
solver.add(Or(
    And(pos['percussionist'] < pos['saxophonist'], pos['trumpeter'] > pos['saxophonist']),
    And(pos['trumpeter'] < pos['saxophonist'], pos['percussionist'] > pos['saxophonist'])
))

# Given condition: violinist performs the fourth solo
solver.add(pos['violinist'] == 4)

# Check satisfiability of the base constraints
base_result = solver.check()
if base_result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (base constraints are unsatisfiable)")
    exit()

# Define the options as constraints
options = {
    "A": pos['percussionist'] < pos['violinist'],  # Percussionist before violinist
    "B": pos['trumpeter'] < pos['violinist'],       # Trumpeter before violinist
    "C": pos['trumpeter'] < pos['guitarist'],       # Trumpeter before guitarist
    "D": pos['saxophonist'] < pos['violinist'],     # Saxophonist before violinist
    "E": pos['trumpeter'] < pos['saxophonist']      # Trumpeter before saxophonist
}

# Check the satisfiability of each option
found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Determine the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")