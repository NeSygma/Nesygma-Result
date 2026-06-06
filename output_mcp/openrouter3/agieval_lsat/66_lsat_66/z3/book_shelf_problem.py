from z3 import *

# Create solver
solver = Solver()

# Define shelf numbers: 1=top, 2=middle, 3=bottom
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {book: Int(f'shelf_{book}') for book in books}

# Base constraints
# Each book is on one of the three shelves
for book in books:
    solver.add(shelf[book] >= 1)
    solver.add(shelf[book] <= 3)

# At least two books per shelf
for s in [1, 2, 3]:
    solver.add(Sum([If(shelf[book] == s, 1, 0) for book in books]) >= 2)

# More books on bottom shelf than top shelf
top_count = Sum([If(shelf[book] == 1, 1, 0) for book in books])
bottom_count = Sum([If(shelf[book] == 3, 1, 0) for book in books])
solver.add(bottom_count > top_count)

# I is placed on the middle shelf
solver.add(shelf['I'] == 2)

# K is placed on a higher shelf than F (higher shelf = larger number)
solver.add(shelf['K'] > shelf['F'])

# O is placed on a higher shelf than L
solver.add(shelf['O'] > shelf['L'])

# F is placed on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# Now test each answer choice
found_options = []

# Option A: Bottom shelf = F, M
opt_a_constr = And(
    shelf['F'] == 3,
    shelf['M'] == 3,
    # Other books not on bottom shelf
    *[shelf[book] != 3 for book in books if book not in ['F', 'M']]
)

# Option B: Bottom shelf = F, H, M
opt_b_constr = And(
    shelf['F'] == 3,
    shelf['H'] == 3,
    shelf['M'] == 3,
    *[shelf[book] != 3 for book in books if book not in ['F', 'H', 'M']]
)

# Option C: Bottom shelf = G, H, K
opt_c_constr = And(
    shelf['G'] == 3,
    shelf['H'] == 3,
    shelf['K'] == 3,
    *[shelf[book] != 3 for book in books if book not in ['G', 'H', 'K']]
)

# Option D: Bottom shelf = F, G, M, O
opt_d_constr = And(
    shelf['F'] == 3,
    shelf['G'] == 3,
    shelf['M'] == 3,
    shelf['O'] == 3,
    *[shelf[book] != 3 for book in books if book not in ['F', 'G', 'M', 'O']]
)

# Option E: Bottom shelf = G, H, L, M
opt_e_constr = And(
    shelf['G'] == 3,
    shelf['H'] == 3,
    shelf['L'] == 3,
    shelf['M'] == 3,
    *[shelf[book] != 3 for book in books if book not in ['G', 'H', 'L', 'M']]
)

# Test each option
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
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