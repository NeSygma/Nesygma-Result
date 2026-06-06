from z3 import *

solver = Solver()

# Book variables: shelf assignment (0=top, 1=middle, 2=bottom)
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(f'shelf_{b}') for b in books}

# Domain constraints: each shelf is 0, 1, or 2
for b in books:
    solver.add(shelf[b] >= 0, shelf[b] <= 2)

# At least two books on each shelf
for s in [0, 1, 2]:
    solver.add(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)

# More books on bottom shelf than top shelf
solver.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) > Sum([If(shelf[b] == 0, 1, 0) for b in books]))

# I is on middle shelf
solver.add(shelf['I'] == 1)

# K is on a higher shelf than F (higher = smaller number)
solver.add(shelf['K'] < shelf['F'])

# O is on a higher shelf than L
solver.add(shelf['O'] < shelf['L'])

# F is on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# Additional constraint: G is on top shelf
solver.add(shelf['G'] == 0)

# Now test each option
# Option constraints: exactly those books are on middle shelf (shelf == 1)
options = {
    "A": ['H', 'I'],
    "B": ['I', 'L'],
    "C": ['H', 'I', 'L'],
    "D": ['I', 'K', 'L'],
    "E": ['F', 'I', 'M']
}

found_options = []

for letter, middle_books in options.items():
    solver.push()
    # For each book in middle_books, it must be on middle shelf
    for b in middle_books:
        solver.add(shelf[b] == 1)
    # For each book NOT in middle_books, it must NOT be on middle shelf
    for b in books:
        if b not in middle_books:
            solver.add(shelf[b] != 1)
    if solver.check() == sat:
        found_options.append(letter)
        # Print model for debugging
        m = solver.model()
        print(f"Option {letter} is SAT. Model:")
        for b in books:
            print(f"  {b}: {m[shelf[b]]}")
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