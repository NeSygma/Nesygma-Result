from z3 import *

# Define books
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']

# Create shelf variables (0: top, 1: middle, 2: bottom)
shelf = {book: Int(book) for book in books}

solver = Solver()

# Domain constraints: each shelf variable in {0,1,2}
for book in books:
    solver.add(shelf[book] >= 0)
    solver.add(shelf[book] <= 2)

# Base constraints
solver.add(shelf['G'] == 0)          # G on top shelf
solver.add(shelf['I'] == 1)          # I on middle shelf
solver.add(shelf['K'] < shelf['F'])  # K higher than F
solver.add(shelf['O'] < shelf['L'])  # O higher than L
solver.add(shelf['F'] == shelf['M']) # F and M on same shelf

# Count books per shelf
count_top = Sum([If(shelf[book] == 0, 1, 0) for book in books])
count_mid = Sum([If(shelf[book] == 1, 1, 0) for book in books])
count_bottom = Sum([If(shelf[book] == 2, 1, 0) for book in books])

# At least two books per shelf
solver.add(count_top >= 2)
solver.add(count_mid >= 2)
solver.add(count_bottom >= 2)

# More books on bottom than top
solver.add(count_bottom > count_top)

# Define option constraints
# Option A: middle shelf = H, I
opt_a_constr = And(
    shelf['H'] == 1,
    shelf['I'] == 1,
    *[shelf[book] != 1 for book in books if book not in ['H', 'I']]
)

# Option B: middle shelf = I, L
opt_b_constr = And(
    shelf['I'] == 1,
    shelf['L'] == 1,
    *[shelf[book] != 1 for book in books if book not in ['I', 'L']]
)

# Option C: middle shelf = H, I, L
opt_c_constr = And(
    shelf['H'] == 1,
    shelf['I'] == 1,
    shelf['L'] == 1,
    *[shelf[book] != 1 for book in books if book not in ['H', 'I', 'L']]
)

# Option D: middle shelf = I, K, L
opt_d_constr = And(
    shelf['I'] == 1,
    shelf['K'] == 1,
    shelf['L'] == 1,
    *[shelf[book] != 1 for book in books if book not in ['I', 'K', 'L']]
)

# Option E: middle shelf = F, I, M
opt_e_constr = And(
    shelf['F'] == 1,
    shelf['I'] == 1,
    shelf['M'] == 1,
    *[shelf[book] != 1 for book in books if book not in ['F', 'I', 'M']]
)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")