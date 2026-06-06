from z3 import *

solver = Solver()

# Declare shelves as integers for ordering: top < middle < bottom
# We'll represent shelves as 0 (top), 1 (middle), 2 (bottom)

# Books: F, G, H, I, K, L, M, O
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']

# Assign each book to a shelf (0: top, 1: middle, 2: bottom)
shelf = {b: Int(f'shelf_{b}') for b in books}

# Each shelf must have at least two books
shelves = [0, 1, 2]
for s in shelves:
    solver.add(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)

# More books on bottom shelf than top shelf
solver.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) > Sum([If(shelf[b] == 0, 1, 0) for b in books]))

# I is on the middle shelf
solver.add(shelf['I'] == 1)

# K is on a higher shelf than F (higher means smaller integer value)
solver.add(shelf['K'] < shelf['F'])

# O is on a higher shelf than L
solver.add(shelf['O'] < shelf['L'])

# F is on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# Enforce a stricter distribution: (2, 2, 4) books per shelf (top, middle, bottom)
solver.add(Sum([If(shelf[b] == 0, 1, 0) for b in books]) == 2)
solver.add(Sum([If(shelf[b] == 1, 1, 0) for b in books]) == 2)
solver.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) == 4)

# Option A: O is placed on a shelf higher than the shelf M is placed on
opt_a_constr = (shelf['O'] < shelf['M'])

# Option B: K is placed on a shelf higher than the shelf G is placed on
opt_b_constr = (shelf['K'] < shelf['G'])

# Option C: I is placed on a shelf higher than the shelf F is placed on
opt_c_constr = (shelf['I'] < shelf['F'])

# Option D: G is placed on a shelf higher than the shelf O is placed on
opt_d_constr = (shelf['G'] < shelf['O'])

# Option E: F is placed on a shelf higher than the shelf L is placed on
opt_e_constr = (shelf['F'] < shelf['L'])

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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