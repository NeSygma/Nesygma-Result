from z3 import *

solver = Solver()

books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
# shelf numbers: 0 = top, 1 = middle, 2 = bottom
shelf = {b: Int(f'shelf_{b}') for b in books}

for b in books:
    solver.add(shelf[b] >= 0, shelf[b] <= 2)

# At least two books on each shelf
for s in range(3):
    solver.add(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)

# More books on bottom than top
bottom_count = Sum([If(shelf[b] == 2, 1, 0) for b in books])
top_count = Sum([If(shelf[b] == 0, 1, 0) for b in books])
solver.add(bottom_count > top_count)

# I is on middle shelf
solver.add(shelf['I'] == 1)

# K higher than F (smaller shelf number = higher)
solver.add(shelf['K'] < shelf['F'])

# O higher than L
solver.add(shelf['O'] < shelf['L'])

# F and M same shelf
solver.add(shelf['F'] == shelf['M'])

# Options
options = [
    ("A", ['F', 'M']),
    ("B", ['F', 'H', 'M']),
    ("C", ['G', 'H', 'K']),
    ("D", ['F', 'G', 'M', 'O']),
    ("E", ['G', 'H', 'L', 'M']),
]

found_options = []

for letter, bottom_list in options:
    solver.push()
    # Books in bottom_list must be on bottom shelf (shelf == 2)
    for b in bottom_list:
        solver.add(shelf[b] == 2)
    # All other books must NOT be on bottom shelf
    other_books = [b for b in books if b not in bottom_list]
    for b in other_books:
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