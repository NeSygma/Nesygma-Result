from z3 import *

solver = Solver()

# Books: F, G, H, I, K, L, M, O
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
n = len(books)

# Shelf assignment: 0 = bottom, 1 = middle, 2 = top
shelf = {b: Int(f'shelf_{b}') for b in books}

# Each book is on exactly one shelf (0, 1, or 2)
for b in books:
    solver.add(shelf[b] >= 0, shelf[b] <= 2)

# At least two books on each shelf
solver.add(Sum([If(shelf[b] == 0, 1, 0) for b in books]) >= 2)
solver.add(Sum([If(shelf[b] == 1, 1, 0) for b in books]) >= 2)
solver.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) >= 2)

# More books on bottom than top
solver.add(Sum([If(shelf[b] == 0, 1, 0) for b in books]) > Sum([If(shelf[b] == 2, 1, 0) for b in books]))

# I is on the middle shelf
solver.add(shelf['I'] == 1)

# K is on a higher shelf than F
solver.add(shelf['K'] > shelf['F'])

# O is on a higher shelf than L
solver.add(shelf['O'] > shelf['L'])

# F is on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# For each option, test if it could be a complete and accurate list of bottom shelf books
# "Complete and accurate" means these are ALL the books on the bottom shelf, no more

options = {
    "A": ['F', 'M'],
    "B": ['F', 'H', 'M'],
    "C": ['G', 'H', 'K'],
    "D": ['F', 'G', 'M', 'O'],
    "E": ['G', 'H', 'L', 'M']
}

found_options = []

for letter, bottom_books in options.items():
    solver.push()
    # The books listed are on the bottom shelf
    for b in bottom_books:
        solver.add(shelf[b] == 0)
    # No other books are on the bottom shelf
    other_books = [b for b in books if b not in bottom_books]
    for b in other_books:
        solver.add(shelf[b] != 0)
    
    if solver.check() == sat:
        found_options.append(letter)
        print(f"Option {letter}: SAT")
        m = solver.model()
        for b in books:
            print(f"  {b} -> shelf {m[shelf[b]]}")
    else:
        print(f"Option {letter}: UNSAT")
    
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