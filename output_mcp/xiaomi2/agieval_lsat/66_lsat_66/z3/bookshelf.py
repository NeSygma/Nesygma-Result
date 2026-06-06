from z3 import *

solver = Solver()

# Books: F, G, H, I, K, L, M, O
# Shelves: top=0, middle=1, bottom=2
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(f'shelf_{b}') for b in books}

# Each book on exactly one shelf (0, 1, or 2)
for b in books:
    solver.add(Or(shelf[b] == 0, shelf[b] == 1, shelf[b] == 2))

# At least 2 books on each shelf
for s in range(3):
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

# Define each answer choice constraint
# For each option: listed books MUST be on bottom (2), others MUST NOT be on bottom
def bottom_is(exact_books):
    constraints = []
    for b in books:
        if b in exact_books:
            constraints.append(shelf[b] == 2)
        else:
            constraints.append(shelf[b] != 2)
    return And(constraints)

options = {
    "A": bottom_is({'F', 'M'}),
    "B": bottom_is({'F', 'H', 'M'}),
    "C": bottom_is({'G', 'H', 'K'}),
    "D": bottom_is({'F', 'G', 'M', 'O'}),
    "E": bottom_is({'G', 'H', 'L', 'M'}),
}

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        m = solver.model()
        found_options.append(letter)
        print(f"Option {letter}: SAT")
        for b in books:
            print(f"  {b} -> shelf {m[shelf[b]]}")
    else:
        print(f"Option {letter}: {result}")
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