from z3 import *

solver = Solver()

# Declare shelves as integers for ordering: top=0, middle=1, bottom=2
# Books are represented as integers for their shelf assignments
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelves = ['top', 'middle', 'bottom']

# Assign each book to a shelf (0=top, 1=middle, 2=bottom)
book_to_shelf = {book: Int(f'{book}_shelf') for book in books}

# Base constraints
# 1. At least two books on each shelf
for shelf in [0, 1, 2]:
    solver.add(Sum([If(book_to_shelf[book] == shelf, 1, 0) for book in books]) >= 2)

# 2. More books on bottom shelf than top shelf
solver.add(Sum([If(book_to_shelf[book] == 2, 1, 0) for book in books]) > 
           Sum([If(book_to_shelf[book] == 0, 1, 0) for book in books]))

# 3. I is on the middle shelf
solver.add(book_to_shelf['I'] == 1)

# 4. K is on a higher shelf than F
solver.add(book_to_shelf['K'] > book_to_shelf['F'])

# 5. O is on a higher shelf than L
solver.add(book_to_shelf['O'] > book_to_shelf['L'])

# 6. F is on the same shelf as M
solver.add(book_to_shelf['F'] == book_to_shelf['M'])

# Evaluate each option
found_options = []

# Option A: I and M are on the same shelf
solver.push()
solver.add(book_to_shelf['I'] == book_to_shelf['M'])
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: K and G are on the same shelf
solver.push()
solver.add(book_to_shelf['K'] == book_to_shelf['G'])
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: L and F are on the same shelf
solver.push()
solver.add(book_to_shelf['L'] == book_to_shelf['F'])
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: M and H are on the same shelf
solver.push()
solver.add(book_to_shelf['M'] == book_to_shelf['H'])
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: H and O are on the same shelf
solver.push()
solver.add(book_to_shelf['H'] == book_to_shelf['O'])
if solver.check() == sat:
    found_options.append("E")
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