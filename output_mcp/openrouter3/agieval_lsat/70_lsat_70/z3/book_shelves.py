from z3 import *

# Create solver
solver = Solver()

# Books: F, G, H, I, K, L, M, O
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {book: Int(f'shelf_{book}') for book in books}

# Shelves are 0 (top), 1 (middle), 2 (bottom)
for book in books:
    solver.add(shelf[book] >= 0)
    solver.add(shelf[book] <= 2)

# Constraint 1: At least 2 books per shelf
# Count books on each shelf
for s in range(3):
    solver.add(Sum([If(shelf[book] == s, 1, 0) for book in books]) >= 2)

# Constraint 2: More books on bottom shelf than top shelf
solver.add(Sum([If(shelf[book] == 2, 1, 0) for book in books]) > 
           Sum([If(shelf[book] == 0, 1, 0) for book in books]))

# Constraint 3: I is on middle shelf (shelf 1)
solver.add(shelf['I'] == 1)

# Constraint 4: K is on a higher shelf than F (K > F)
solver.add(shelf['K'] > shelf['F'])

# Constraint 5: O is on a higher shelf than L (O > L)
solver.add(shelf['O'] > shelf['L'])

# Constraint 6: F and M are on the same shelf
solver.add(shelf['F'] == shelf['M'])

# Additional condition: L is placed on a shelf higher than H (L > H)
solver.add(shelf['L'] > shelf['H'])

# Now test each option
# Option A: F and G are placed on the same shelf as each other
opt_a_constr = (shelf['F'] == shelf['G'])

# Option B: G and H are placed on the same shelf as each other
opt_b_constr = (shelf['G'] == shelf['H'])

# Option C: H and M are placed on the same shelf as each other
opt_c_constr = (shelf['H'] == shelf['M'])

# Option D: I and G are placed on the same shelf as each other
opt_d_constr = (shelf['I'] == shelf['G'])

# Option E: K and O are placed on the same shelf as each other
opt_e_constr = (shelf['K'] == shelf['O'])

# Test each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
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