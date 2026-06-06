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

# Now evaluate each answer choice for MUST BE TRUE
found_options = []

# Option A: O is placed on a shelf higher than the shelf M is placed on
# Check if NOT(A) is unsatisfiable
solver.push()
solver.add(Not(shelf['O'] > shelf['M']))
result_a = solver.check()
solver.pop()
if result_a == unsat:
    found_options.append('A')

# Option B: K is placed on a shelf higher than the shelf G is placed on
solver.push()
solver.add(Not(shelf['K'] > shelf['G']))
result_b = solver.check()
solver.pop()
if result_b == unsat:
    found_options.append('B')

# Option C: I is placed on a shelf higher than the shelf F is placed on
solver.push()
solver.add(Not(shelf['I'] > shelf['F']))
result_c = solver.check()
solver.pop()
if result_c == unsat:
    found_options.append('C')

# Option D: G is placed on a shelf higher than the shelf O is placed on
solver.push()
solver.add(Not(shelf['G'] > shelf['O']))
result_d = solver.check()
solver.pop()
if result_d == unsat:
    found_options.append('D')

# Option E: F is placed on a shelf higher than the shelf L is placed on
solver.push()
solver.add(Not(shelf['F'] > shelf['L']))
result_e = solver.check()
solver.pop()
if result_e == unsat:
    found_options.append('E')

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