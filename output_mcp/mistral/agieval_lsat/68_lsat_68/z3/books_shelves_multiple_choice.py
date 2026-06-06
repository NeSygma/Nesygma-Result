from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare shelves as integers: 0=Top, 1=Middle, 2=Bottom
solver = Solver()

# Books
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']

# Assign each book to a shelf (0=Top, 1=Middle, 2=Bottom)
shelf = {book: Int(f'shelf_{book}') for book in books}

# Each book is on exactly one shelf
for book in books:
    solver.add(shelf[book] >= 0, shelf[book] <= 2)

# At least two books on each shelf
for s in [0, 1, 2]:
    solver.add(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)

# More books on the bottom shelf (2) than the top shelf (0)
solver.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) > Sum([If(shelf[b] == 0, 1, 0) for b in books]))

# I is on the middle shelf
solver.add(shelf['I'] == 1)

# K is on a higher shelf than F
solver.add(shelf['K'] > shelf['F'])

# O is on a higher shelf than L
solver.add(shelf['O'] > shelf['L'])

# F is on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# Base constraints are now set. Now evaluate the multiple-choice options.

# Define the constraints for each option
# (A) O is placed on a shelf higher than the shelf M is placed on.
opt_a_constr = (shelf['O'] > shelf['M'])

# (B) K is placed on a shelf higher than the shelf G is placed on.
opt_b_constr = (shelf['K'] > shelf['G'])

# (C) I is placed on a shelf higher than the shelf F is placed on.
opt_c_constr = (shelf['I'] > shelf['F'])

# (D) G is placed on a shelf higher than the shelf O is placed on.
opt_d_constr = (shelf['G'] > shelf['O'])

# (E) F is placed on a shelf higher than the shelf L is placed on.
opt_e_constr = (shelf['F'] > shelf['L'])

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Decide the output based on the number of valid options
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")