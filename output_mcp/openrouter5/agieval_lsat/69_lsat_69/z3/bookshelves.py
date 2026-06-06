from z3 import *

# Books: F, G, H, I, K, L, M, O
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
n = len(books)

# Shelves: 0 = top, 1 = middle, 2 = bottom
shelf = {b: Int(f'shelf_{b}') for b in books}

solver = Solver()

# Each book is on exactly one shelf: 0 (top), 1 (middle), or 2 (bottom)
for b in books:
    solver.add(shelf[b] >= 0, shelf[b] <= 2)

# At least two books on each shelf
for s in range(3):
    solver.add(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)

# More books on bottom shelf than top shelf
solver.add(
    Sum([If(shelf[b] == 2, 1, 0) for b in books]) >
    Sum([If(shelf[b] == 0, 1, 0) for b in books])
)

# I is on the middle shelf
solver.add(shelf['I'] == 1)

# K is on a higher shelf than F (higher = smaller number)
solver.add(shelf['K'] < shelf['F'])

# O is on a higher shelf than L
solver.add(shelf['O'] < shelf['L'])

# F is on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# Additional condition: G is on the top shelf
solver.add(shelf['G'] == 0)

# Now evaluate each option as a complete and accurate list of books on the middle shelf.
# "Complete and accurate" means: the set of books on the middle shelf is exactly that list.
# So we add constraint: for each book, it's on middle shelf iff it's in the given list.

options = {
    "A": ['H', 'I'],
    "B": ['I', 'L'],
    "C": ['H', 'I', 'L'],
    "D": ['I', 'K', 'L'],
    "E": ['F', 'I', 'M']
}

found_options = []

for letter, mid_books in options.items():
    solver.push()
    # For each book, it's on middle shelf (shelf == 1) iff it's in mid_books
    for b in books:
        if b in mid_books:
            solver.add(shelf[b] == 1)
        else:
            solver.add(shelf[b] != 1)
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