from z3 import *

# Create solver
solver = Solver()

# Books and shelves
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf_numbers = [1, 2, 3]  # 1=top, 2=middle, 3=bottom

# Create shelf assignment variables for each book
shelf = {book: Int(f'shelf_{book}') for book in books}

# Domain constraints: each book on shelf 1, 2, or 3
for book in books:
    solver.add(shelf[book] >= 1)
    solver.add(shelf[book] <= 3)

# At least 2 books per shelf
for s in shelf_numbers:
    solver.add(Sum([If(shelf[book] == s, 1, 0) for book in books]) >= 2)

# Condition 1: More books on bottom shelf than top shelf
bottom_count = Sum([If(shelf[book] == 3, 1, 0) for book in books])
top_count = Sum([If(shelf[book] == 1, 1, 0) for book in books])
solver.add(bottom_count > top_count)

# Condition 2: I is on middle shelf
solver.add(shelf['I'] == 2)

# Condition 3: K is on a higher shelf than F (K < F in shelf number)
solver.add(shelf['K'] < shelf['F'])

# Condition 4: O is on a higher shelf than L (O < L in shelf number)
solver.add(shelf['O'] < shelf['L'])

# Condition 5: F is on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# Additional condition: G is on the top shelf
solver.add(shelf['G'] == 1)

# Now test each answer choice
# Each choice gives a list of books that should be exactly the middle shelf books
# We need to check if there's a valid assignment where the middle shelf contains exactly those books

# Define the options
options = {
    'A': ['H', 'I'],
    'B': ['I', 'L'],
    'C': ['H', 'I', 'L'],
    'D': ['I', 'K', 'L'],
    'E': ['F', 'I', 'M']
}

found_options = []

for letter, middle_books in options.items():
    solver.push()
    
    # Constraint: exactly these books are on the middle shelf (shelf 2)
    # First, these books must be on shelf 2
    for book in middle_books:
        solver.add(shelf[book] == 2)
    
    # Second, no other books can be on shelf 2
    for book in books:
        if book not in middle_books:
            solver.add(shelf[book] != 2)
    
    # Check if this is satisfiable
    if solver.check() == sat:
        found_options.append(letter)
    
    solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")