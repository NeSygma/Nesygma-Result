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
for s in range(3):
    solver.add(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)

# More books on bottom shelf (2) than top shelf (0)
solver.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) > 
           Sum([If(shelf[b] == 0, 1, 0) for b in books]))

# I is on the middle shelf (1)
solver.add(shelf['I'] == 1)

# K is on a higher shelf than F (higher = smaller number)
solver.add(shelf['K'] < shelf['F'])

# O is on a higher shelf than L
solver.add(shelf['O'] < shelf['L'])

# F is on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# Additional condition from the question: L is on a higher shelf than H
solver.add(shelf['L'] < shelf['H'])

# Now evaluate each option
# Option A: F and G are on the same shelf
opt_a = (shelf['F'] == shelf['G'])

# Option B: G and H are on the same shelf
opt_b = (shelf['G'] == shelf['H'])

# Option C: H and M are on the same shelf
opt_c = (shelf['H'] == shelf['M'])

# Option D: I and G are on the same shelf
opt_d = (shelf['I'] == shelf['G'])

# Option E: K and O are on the same shelf
opt_e = (shelf['K'] == shelf['O'])

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