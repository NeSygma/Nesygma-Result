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

# K is placed on a higher shelf than F (higher = smaller number: top=0 > middle=1 > bottom=2)
solver.add(shelf['K'] < shelf['F'])

# O is placed on a higher shelf than L
solver.add(shelf['O'] < shelf['L'])

# F is placed on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# Now test each answer choice for what's on the bottom shelf
# We need to check if the given list COULD be the complete and accurate list of books on the bottom shelf

def make_bottom_constraint(book_list):
    """Create constraint: exactly these books are on the bottom shelf, and no others"""
    constraints = []
    for b in books:
        if b in book_list:
            constraints.append(shelf[b] == 2)
        else:
            constraints.append(shelf[b] != 2)
    return And(constraints)

options = {
    "A": ["F", "M"],
    "B": ["F", "H", "M"],
    "C": ["G", "H", "K"],
    "D": ["F", "G", "M", "O"],
    "E": ["G", "H", "L", "M"],
}

found_options = []
for letter, book_list in options.items():
    solver.push()
    solver.add(make_bottom_constraint(book_list))
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for b in books:
            print(f"  {b} -> shelf {m[shelf[b]]}")
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