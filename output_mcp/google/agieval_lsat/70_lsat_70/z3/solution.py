from z3 import *

# Books: F, G, H, I, K, L, M, O
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
# Shelves: 0=Top, 1=Middle, 2=Bottom
# Higher shelf means lower index.

shelf = {b: Int(f'shelf_{b}') for b in books}
solver = Solver()

# Domain constraints
for b in books:
    solver.add(shelf[b] >= 0, shelf[b] <= 2)

# At least 2 books per shelf
for s in range(3):
    solver.add(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)

# Total books = 8
solver.add(Sum([1 for b in books]) == 8)

# More books on bottom than top
count_top = Sum([If(shelf[b] == 0, 1, 0) for b in books])
count_bottom = Sum([If(shelf[b] == 2, 1, 0) for b in books])
solver.add(count_bottom > count_top)

# I is on the middle shelf
solver.add(shelf['I'] == 1)

# K is on a higher shelf than F (shelf[K] < shelf[F])
solver.add(shelf['K'] < shelf['F'])

# O is on a higher shelf than L (shelf[O] < shelf[L])
solver.add(shelf['O'] < shelf['L'])

# F is on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# Question condition: L is on a higher shelf than H (shelf[L] < shelf[H])
solver.add(shelf['L'] < shelf['H'])

# Options
# (A) F and G are on the same shelf
# (B) G and H are on the same shelf
# (C) H and M are on the same shelf
# (D) I and G are on the same shelf
# (E) K and O are on the same shelf

opt_a = (shelf['F'] == shelf['G'])
opt_b = (shelf['G'] == shelf['H'])
opt_c = (shelf['H'] == shelf['M'])
opt_d = (shelf['I'] == shelf['G'])
opt_e = (shelf['K'] == shelf['O'])

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(Not(constr))
    # If Not(constr) is unsat, then constr must be true in all valid models
    if solver.check() == unsat:
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