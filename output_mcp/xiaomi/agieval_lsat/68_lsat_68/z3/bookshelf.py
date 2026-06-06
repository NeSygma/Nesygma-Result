from z3 import *

solver = Solver()

# Books: F, G, H, I, K, L, M, O
# Shelves: 0 = top, 1 = middle, 2 = bottom
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(f'shelf_{b}') for b in books}

# Each book is on shelf 0, 1, or 2
for b in books:
    solver.add(Or(shelf[b] == 0, shelf[b] == 1, shelf[b] == 2))

# At least two books on each shelf
for s in range(3):
    solver.add(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)

# More books on bottom shelf than top shelf
solver.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) > Sum([If(shelf[b] == 0, 1, 0) for b in books]))

# I is placed on the middle shelf
solver.add(shelf['I'] == 1)

# K is placed on a higher shelf than F (higher = smaller number: top=0 > middle=1 > bottom=2)
solver.add(shelf['K'] < shelf['F'])

# O is placed on a higher shelf than L
solver.add(shelf['O'] < shelf['L'])

# F is placed on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# Define option constraints
# (A) O is placed on a shelf higher than the shelf M is placed on
opt_a = shelf['O'] < shelf['M']

# (B) K is placed on a shelf higher than the shelf G is placed on
opt_b = shelf['K'] < shelf['G']

# (C) I is placed on a shelf higher than the shelf F is placed on
opt_c = shelf['I'] < shelf['F']

# (D) G is placed on a shelf higher than the shelf O is placed on
opt_d = shelf['G'] < shelf['O']

# (E) F is placed on a shelf higher than the shelf L is placed on
opt_e = shelf['F'] < shelf['L']

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
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