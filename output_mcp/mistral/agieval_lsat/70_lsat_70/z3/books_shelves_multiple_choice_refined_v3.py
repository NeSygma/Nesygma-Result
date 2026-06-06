from z3 import *

# Declare symbolic variables for each book's shelf
# 0 = top, 1 = middle, 2 = bottom
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(f'shelf_{b}') for b in books}

solver = Solver()

# Base constraints
# 1. At least two books per shelf
for s in [0, 1, 2]:
    solver.add(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)

# 2. More books on bottom shelf than top shelf
solver.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) > Sum([If(shelf[b] == 0, 1, 0) for b in books]))

# 3. I is on the middle shelf
solver.add(shelf['I'] == 1)

# 4. K is on a higher shelf than F
solver.add(shelf['K'] > shelf['F'])

# 5. O is on a higher shelf than L
solver.add(shelf['O'] > shelf['L'])

# 6. F is on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# Additional constraint for the question: L is on a shelf higher than H
solver.add(shelf['L'] > shelf['H'])

# Define the options as constraints
opt_a_constr = (shelf['F'] == shelf['G'])
opt_b_constr = (shelf['G'] == shelf['H'])
opt_c_constr = (shelf['H'] == shelf['M'])
opt_d_constr = (shelf['I'] == shelf['G'])
opt_e_constr = (shelf['K'] == shelf['O'])

# Evaluate each option for entailment (must be true in all models)
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    # Check if the option is necessarily true: if the constraints imply the option
    # We do this by checking if the negation of the option is unsatisfiable with the constraints
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        # If the negation is unsatisfiable, the option must be true
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")