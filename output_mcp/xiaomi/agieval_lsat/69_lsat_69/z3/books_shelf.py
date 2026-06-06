from z3 import *

solver = Solver()

# Books: F, G, H, I, K, L, M, O
# Shelves: 0 = top, 1 = middle, 2 = bottom
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(f'shelf_{b}') for b in books}

# Each book on exactly one shelf (0, 1, or 2)
for b in books:
    solver.add(Or(shelf[b] == 0, shelf[b] == 1, shelf[b] == 2))

# At least two books on each shelf
for s in range(3):
    solver.add(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)

# More books on bottom shelf than top shelf
solver.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) > Sum([If(shelf[b] == 0, 1, 0) for b in books]))

# I is placed on the middle shelf
solver.add(shelf['I'] == 1)

# K is placed on a higher shelf than F (lower number = higher shelf)
solver.add(shelf['K'] < shelf['F'])

# O is placed on a higher shelf than L
solver.add(shelf['O'] < shelf['L'])

# F is placed on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# G is placed on the top shelf
solver.add(shelf['G'] == 0)

# Define option constraints: the middle shelf contains EXACTLY the listed books
# Option A: H, I on middle shelf (and no others)
def exact_middle(middle_books):
    constraints = []
    for b in books:
        if b in middle_books:
            constraints.append(shelf[b] == 1)
        else:
            constraints.append(shelf[b] != 1)
    return And(constraints)

opt_a_constr = exact_middle(['H', 'I'])
opt_b_constr = exact_middle(['I', 'L'])
opt_c_constr = exact_middle(['H', 'I', 'L'])
opt_d_constr = exact_middle(['I', 'K', 'L'])
opt_e_constr = exact_middle(['F', 'I', 'M'])

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