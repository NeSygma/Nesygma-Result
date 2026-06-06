from z3 import *

# Exactly eight books: F, G, H, I, K, L, M, O
# Three shelves: top (0), middle (1), bottom (2)
# Higher shelf = smaller number (top=0 is highest, bottom=2 is lowest)

solver = Solver()

# Variables: shelf assignment for each book (0=top, 1=middle, 2=bottom)
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(f'shelf_{b}') for b in books}

# Domain: each shelf is 0, 1, or 2
for b in books:
    solver.add(shelf[b] >= 0, shelf[b] <= 2)

# At least two books on each shelf
solver.add(Sum([If(shelf[b] == 0, 1, 0) for b in books]) >= 2)
solver.add(Sum([If(shelf[b] == 1, 1, 0) for b in books]) >= 2)
solver.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) >= 2)

# More books on bottom shelf than top shelf
solver.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) > Sum([If(shelf[b] == 0, 1, 0) for b in books]))

# I is placed on the middle shelf
solver.add(shelf['I'] == 1)

# K is placed on a higher shelf than F (higher = smaller number)
solver.add(shelf['K'] < shelf['F'])

# O is placed on a higher shelf than L
solver.add(shelf['O'] < shelf['L'])

# F is placed on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# Now evaluate each option
# Option A: O is placed on a shelf higher than the shelf M is placed on.
# O < M
opt_a = shelf['O'] < shelf['M']

# Option B: K is placed on a shelf higher than the shelf G is placed on.
# K < G
opt_b = shelf['K'] < shelf['G']

# Option C: I is placed on a shelf higher than the shelf F is placed on.
# I < F (I=1, so F must be on bottom shelf 2)
opt_c = shelf['I'] < shelf['F']

# Option D: G is placed on a shelf higher than the shelf O is placed on.
# G < O
opt_d = shelf['G'] < shelf['O']

# Option E: F is placed on a shelf higher than the shelf L is placed on.
# F < L
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