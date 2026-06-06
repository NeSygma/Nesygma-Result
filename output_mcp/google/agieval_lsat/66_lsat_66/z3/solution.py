from z3 import *

# Books
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
# Shelves: 1=Top, 2=Middle, 3=Bottom
shelf = {b: Int(f'shelf_{b}') for b in books}

solver = Solver()

# Domain constraints
for b in books:
    solver.add(shelf[b] >= 1, shelf[b] <= 3)

# At least 2 books per shelf
for s in [1, 2, 3]:
    solver.add(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)

# Total books = 8
solver.add(Sum([1 for b in books]) == 8)

# More books on bottom than top
count_top = Sum([If(shelf[b] == 1, 1, 0) for b in books])
count_bottom = Sum([If(shelf[b] == 3, 1, 0) for b in books])
solver.add(count_bottom > count_top)

# I is on the middle shelf
solver.add(shelf['I'] == 2)

# K is on a higher shelf than F (Shelf(K) < Shelf(F))
solver.add(shelf['K'] < shelf['F'])

# O is on a higher shelf than L (Shelf(O) < Shelf(L))
solver.add(shelf['O'] < shelf['L'])

# F is on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# Options
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
    # Constraint: exactly these books are on the bottom shelf
    for b in books:
        if b in bottom_books:
            solver.add(shelf[b] == 3)
        else:
            solver.add(shelf[b] != 3)
    
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