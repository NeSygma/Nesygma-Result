from z3 import *

# Base constraints solver
solver = Solver()

# Declare the compositions as Int variables representing their positions (1-8)
compositions = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
pos = {c: Int(f'pos_{c}') for c in compositions}

# All positions are distinct and in the range 1-8
solver.add(Distinct(list(pos.values())))
for c in compositions:
    solver.add(pos[c] >= 1, pos[c] <= 8)

# Constraint 1: T is immediately before F or immediately after R
# T immediately before F: pos[T] + 1 == pos[F]
# T immediately after R: pos[R] + 1 == pos[T]
solver.add(Or(pos['T'] + 1 == pos['F'], pos['R'] + 1 == pos['T']))

# Constraint 2: At least two compositions are performed either after F and before R, or after R and before F
# This means the absolute difference between pos[F] and pos[R] must be at least 3
solver.add(Abs(pos['F'] - pos['R']) >= 3)

# Constraint 3: O is performed either first or fifth
solver.add(Or(pos['O'] == 1, pos['O'] == 5))

# Constraint 4: The eighth composition performed is either L or H
solver.add(Or(pos['L'] == 8, pos['H'] == 8))

# Constraint 5: P is performed at some time before S
solver.add(pos['P'] < pos['S'])

# Constraint 6: At least one composition is performed either after O and before S, or after S and before O
# This means the absolute difference between pos[O] and pos[S] must be at least 2
solver.add(Abs(pos['O'] - pos['S']) >= 2)

# Helper function to check if a given option satisfies all constraints
def check_option(option_letter, order):
    # Create a solver instance for this option
    opt_solver = Solver()
    
    # Assign positions based on the order
    for idx, comp in enumerate(order):
        opt_solver.add(pos[comp] == idx + 1)
    
    # Check if all constraints are satisfied
    result = opt_solver.check()
    return result == sat

# Define the options as lists of compositions in order
options = {
    "A": ['L', 'P', 'S', 'R', 'O', 'T', 'F', 'H'],
    "B": ['O', 'T', 'P', 'F', 'S', 'H', 'R', 'L'],
    "C": ['P', 'T', 'F', 'S', 'L', 'R', 'O', 'H'],
    "D": ['P', 'T', 'F', 'S', 'O', 'R', 'L', 'H'],
    "E": ['T', 'F', 'P', 'R', 'O', 'L', 'S', 'H']
}

# Evaluate each option
found_options = []
for letter, order in options.items():
    solver.push()
    if check_option(letter, order):
        found_options.append(letter)
    solver.pop()

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