from z3 import *

# Books and shelves
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(f'shelf_{b}') for b in books}

solver = Solver()

# Shelf numbers: 1 = top, 2 = middle, 3 = bottom
for b in books:
    solver.add(shelf[b] >= 1, shelf[b] <= 3)

# At least 2 books per shelf
for s in [1, 2, 3]:
    solver.add(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)

# More books on bottom shelf than top shelf
bottom_count = Sum([If(shelf[b] == 3, 1, 0) for b in books])
top_count = Sum([If(shelf[b] == 1, 1, 0) for b in books])
solver.add(bottom_count > top_count)

# I is on middle shelf
solver.add(shelf['I'] == 2)

# K is on a higher shelf than F (higher shelf = larger number)
solver.add(shelf['K'] > shelf['F'])

# O is on a higher shelf than L
solver.add(shelf['O'] > shelf['L'])

# F is on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# Now evaluate each answer choice
found_options = []

# Option A: O is placed on a shelf higher than the shelf M is placed on
opt_a_constr = (shelf['O'] > shelf['M'])
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: K is placed on a shelf higher than the shelf G is placed on
opt_b_constr = (shelf['K'] > shelf['G'])
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: I is placed on a shelf higher than the shelf F is placed on
opt_c_constr = (shelf['I'] > shelf['F'])
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: G is placed on a shelf higher than the shelf O is placed on
opt_d_constr = (shelf['G'] > shelf['O'])
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: F is placed on a shelf higher than the shelf L is placed on
opt_e_constr = (shelf['F'] > shelf['L'])
solver.push()
solver.add(opt_e_constr)
if solver.check() == sat:
    found_options.append('E')
solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")