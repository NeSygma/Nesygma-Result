from z3 import *

solver = Solver()

# Declare symbolic variables for the shelves
# We have 8 books: F, G, H, I, K, L, M, O
# Each book is assigned to a shelf: 0=top, 1=middle, 2=bottom
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(f'shelf_{b}') for b in books}

# Helper function to count books on a shelf
def count_books_on_shelf(s):
    return Sum([If(shelf[b] == s, 1, 0) for b in books])

# At least two books on each shelf
top_count = count_books_on_shelf(0)
middle_count = count_books_on_shelf(1)
bottom_count = count_books_on_shelf(2)

solver.add(top_count >= 2)
solver.add(middle_count >= 2)
solver.add(bottom_count >= 2)

# More books on the bottom shelf than the top shelf
solver.add(bottom_count > top_count)

# I is placed on the middle shelf
solver.add(shelf['I'] == 1)

# K is placed on a higher shelf than F
solver.add(shelf['K'] < shelf['F'])

# O is placed on a higher shelf than L
solver.add(shelf['O'] < shelf['L'])

# F is placed on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# Now, evaluate the multiple choice options for the bottom shelf
found_options = []

# Option A: F, M
opt_a_constr = And(
    shelf['F'] == 2,
    shelf['M'] == 2,
    bottom_count == 2
)

# Option B: F, H, M
opt_b_constr = And(
    shelf['F'] == 2,
    shelf['M'] == 2,
    shelf['H'] == 2,
    bottom_count == 3
)

# Option C: G, H, K
opt_c_constr = And(
    shelf['G'] == 2,
    shelf['H'] == 2,
    shelf['K'] == 2,
    bottom_count == 3
)

# Option D: F, G, M, O
opt_d_constr = And(
    shelf['F'] == 2,
    shelf['G'] == 2,
    shelf['M'] == 2,
    shelf['O'] == 2,
    bottom_count == 4
)

# Option E: G, H, L, M
opt_e_constr = And(
    shelf['G'] == 2,
    shelf['H'] == 2,
    shelf['L'] == 2,
    shelf['M'] == 2,
    bottom_count == 4
)

# Evaluate each option
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
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