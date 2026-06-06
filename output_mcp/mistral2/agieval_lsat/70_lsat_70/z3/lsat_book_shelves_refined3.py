from z3 import *

# Initialize solver
solver = Solver()

# Declare shelf assignments for each book (0=Top, 1=Middle, 2=Bottom)
shelves = {
    'F': Int('F'),
    'G': Int('G'),
    'H': Int('H'),
    'I': Int('I'),
    'K': Int('K'),
    'L': Int('L'),
    'M': Int('M'),
    'O': Int('O'),
}

# Base constraints
shelves_list = list(shelves.values())

# At least two books per shelf
for shelf in range(3):
    solver.add(Sum([If(s == shelf, 1, 0) for s in shelves_list]) >= 2)

# More books on bottom shelf than top shelf
top_books = Sum([If(s == 0, 1, 0) for s in shelves_list])
bottom_books = Sum([If(s == 2, 1, 0) for s in shelves_list])
solver.add(bottom_books > top_books)

# I is on the middle shelf
solver.add(shelves['I'] == 1)

# K is on a higher shelf than F
solver.add(shelves['K'] > shelves['F'])

# O is on a higher shelf than L
solver.add(shelves['O'] > shelves['L'])

# F and M are on the same shelf
solver.add(shelves['F'] == shelves['M'])

# Additional condition: L is on a shelf higher than the shelf H is on
solver.add(shelves['L'] > shelves['H'])

# Define the options as constraints
def opt_a_constr():
    return shelves['F'] == shelves['G']

def opt_b_constr():
    return shelves['G'] == shelves['H']

def opt_c_constr():
    return shelves['H'] == shelves['M']

def opt_d_constr():
    return shelves['I'] == shelves['G']

def opt_e_constr():
    return shelves['K'] == shelves['O']

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr())
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