from z3 import *

# Books: F, G, H, I, K, L, M, O
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
n = len(books)

# Shelves: 0 = top, 1 = middle, 2 = bottom
shelf = {b: Int(f'shelf_{b}') for b in books}

solver = Solver()

# Each book is on exactly one shelf: 0 (top), 1 (middle), 2 (bottom)
for b in books:
    solver.add(Or([shelf[b] == s for s in [0, 1, 2]]))

# At least two books on each shelf
for s in [0, 1, 2]:
    solver.add(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)

# More books on bottom shelf than top shelf
solver.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) > Sum([If(shelf[b] == 0, 1, 0) for b in books]))

# I is on the middle shelf
solver.add(shelf['I'] == 1)

# K is on a higher shelf than F (higher = smaller number)
solver.add(shelf['K'] < shelf['F'])

# O is on a higher shelf than L
solver.add(shelf['O'] < shelf['L'])

# F is on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# Now evaluate each option: the option gives a complete list of books on the bottom shelf.
# We need to check if there exists a valid assignment where the bottom shelf contains exactly those books (and possibly others? 
# The question says "complete and accurate list of the books placed on the bottom shelf".
# That means the list includes ALL books on the bottom shelf, no more, no less.
# So we add constraints that the books in the option are on shelf 2, and all other books are NOT on shelf 2.

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
    # Books in the list are on bottom shelf
    for b in bottom_books:
        solver.add(shelf[b] == 2)
    # Books NOT in the list are NOT on bottom shelf
    for b in books:
        if b not in bottom_books:
            solver.add(shelf[b] != 2)
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