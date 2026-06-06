from z3 import *

solver = Solver()

# Shelves: top=0, middle=1, bottom=2
# "higher shelf" means smaller number
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(f'shelf_{b}') for b in books}

# Each book on one of 3 shelves
for b in books:
    solver.add(Or(shelf[b] == 0, shelf[b] == 1, shelf[b] == 2))

# At least 2 books on each shelf
for s in range(3):
    solver.add(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)

# More books on bottom shelf (2) than top shelf (0)
solver.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) > Sum([If(shelf[b] == 0, 1, 0) for b in books]))

# I is on the middle shelf
solver.add(shelf['I'] == 1)

# K is on a higher shelf than F (K < F)
solver.add(shelf['K'] < shelf['F'])

# O is on a higher shelf than L (O < L)
solver.add(shelf['O'] < shelf['L'])

# F is on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# Additional condition: L is on a higher shelf than H (L < H)
solver.add(shelf['L'] < shelf['H'])

# Define answer choice constraints
# (A) F and G are on the same shelf
opt_a = (shelf['F'] == shelf['G'])
# (B) G and H are on the same shelf
opt_b = (shelf['G'] == shelf['H'])
# (C) H and M are on the same shelf
opt_c = (shelf['H'] == shelf['M'])
# (D) I and G are on the same shelf
opt_d = (shelf['G'] == 1)  # I is on middle shelf (1)
# (E) K and O are on the same shelf
opt_e = (shelf['K'] == shelf['O'])

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    # Check if the negation is unsatisfiable (i.e., the option MUST be true)
    solver.add(Not(constr))
    result = solver.check()
    if result == unsat:
        # The option must be true in all valid models
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