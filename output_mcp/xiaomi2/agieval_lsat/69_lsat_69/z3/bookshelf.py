from z3 import *

# Books: F, G, H, I, K, L, M, O
# Shelves: 0=top, 1=middle, 2=bottom
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(f'shelf_{b}') for b in books}

solver = Solver()

# Each book on shelf 0, 1, or 2
for b in books:
    solver.add(Or(shelf[b] == 0, shelf[b] == 1, shelf[b] == 2))

# At least 2 books on each shelf
for s in [0, 1, 2]:
    solver.add(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)

# More books on bottom shelf than top shelf
solver.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) > Sum([If(shelf[b] == 0, 1, 0) for b in books]))

# I is on the middle shelf
solver.add(shelf['I'] == 1)

# K is on a higher shelf than F (lower number = higher shelf)
solver.add(shelf['K'] < shelf['F'])

# O is on a higher shelf than L
solver.add(shelf['O'] < shelf['L'])

# F is on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# G is on the top shelf (given condition)
solver.add(shelf['G'] == 0)

# Define each option as a complete and accurate list of books on the middle shelf
# Option A: Middle shelf has exactly H, I
def exact_middle(middle_books):
    """Returns constraint that middle shelf has exactly these books and no others"""
    constraints = []
    for b in books:
        if b in middle_books:
            constraints.append(shelf[b] == 1)
        else:
            constraints.append(shelf[b] != 1)
    return And(constraints)

opt_a = exact_middle(['H', 'I'])
opt_b = exact_middle(['I', 'L'])
opt_c = exact_middle(['H', 'I', 'L'])
opt_d = exact_middle(['I', 'K', 'L'])
opt_e = exact_middle(['F', 'I', 'M'])

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        m = solver.model()
        found_options.append(letter)
        print(f"Option {letter}: SAT - shelf assignments: ", end="")
        for b in books:
            print(f"{b}={m[shelf[b]]}", end=" ")
        print()
    else:
        print(f"Option {letter}: {result}")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")