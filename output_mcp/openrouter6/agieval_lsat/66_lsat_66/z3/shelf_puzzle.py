from z3 import *

# Define books
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(f'shelf_{b}') for b in books}

solver = Solver()

# Base constraints: each shelf between 1 and 3
for b in books:
    solver.add(shelf[b] >= 1, shelf[b] <= 3)

# At least two books per shelf
for s in [1, 2, 3]:
    count_s = Sum([If(shelf[b] == s, 1, 0) for b in books])
    solver.add(count_s >= 2)

# More books on bottom than top
count_top = Sum([If(shelf[b] == 1, 1, 0) for b in books])
count_bottom = Sum([If(shelf[b] == 3, 1, 0) for b in books])
solver.add(count_bottom > count_top)

# I is on middle shelf
solver.add(shelf['I'] == 2)

# K is on a higher shelf than F (higher shelf means smaller number)
solver.add(shelf['K'] < shelf['F'])

# O is on a higher shelf than L
solver.add(shelf['O'] < shelf['L'])

# F and M on same shelf
solver.add(shelf['F'] == shelf['M'])

# Define options as lists of books for bottom shelf
options = {
    'A': ['F', 'M'],
    'B': ['F', 'H', 'M'],
    'C': ['G', 'H', 'K'],
    'D': ['F', 'G', 'M', 'O'],
    'E': ['G', 'H', 'L', 'M']
}

found_options = []
for letter, bottom_books in options.items():
    solver.push()
    # Bottom shelf exactly these books
    for b in books:
        if b in bottom_books:
            solver.add(shelf[b] == 3)
        else:
            solver.add(shelf[b] != 3)
    # Check satisfiability
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