from z3 import *

# Define position variables for each clue
pos = {c: Int(f'pos_{c}') for c in ['R','S','T','U','W','X','Z']}
solver = Solver()
# Domain constraints: positions 1..7 and all distinct
for v in pos.values():
    solver.add(v >= 1, v <= 7)
solver.add(Distinct(list(pos.values())))
# Base constraints
solver.add(pos['T'] != 1)               # T not in chapter 1
solver.add(pos['W'] == pos['T'] + 3)    # exactly two chapters between T and W (W = T+3)
# S and Z not adjacent
solver.add(Not(Or(pos['S'] - pos['Z'] == 1, pos['Z'] - pos['S'] == 1)))
# W and X not adjacent
solver.add(Not(Or(pos['W'] - pos['X'] == 1, pos['X'] - pos['W'] == 1)))
# U and X must be adjacent
solver.add(Or(pos['U'] - pos['X'] == 1, pos['X'] - pos['U'] == 1))

# Define the options as lists (1-indexed positions)
options = {
    'A': ['S','T','Z','X','U','W','R'],
    'B': ['T','X','U','W','S','R','Z'],
    'C': ['U','S','X','T','Z','R','W'],
    'D': ['X','U','T','Z','R','W','S'],
    'E': ['Z','R','T','U','X','W','S']
}

found_options = []
for letter, order in options.items():
    # Build constraints that each clue is at its position in this order
    opt_constr = []
    for idx, clue in enumerate(order, start=1):
        opt_constr.append(pos[clue] == idx)
    # Combine with base constraints already in solver
    solver.push()
    solver.add(opt_constr)
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