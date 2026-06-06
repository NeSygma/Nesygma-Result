from z3 import *

solver = Solver()

# Shelves: 0=bottom, 1=middle, 2=top
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(f'shelf_{b}') for b in books}

# Each book is on exactly one shelf (0, 1, or 2)
for b in books:
    solver.add(shelf[b] >= 0)
    solver.add(shelf[b] <= 2)

# Constraint 1: At least 2 books per shelf
# Count books on each shelf
top_count = Sum([If(shelf[b] == 2, 1, 0) for b in books])
mid_count = Sum([If(shelf[b] == 1, 1, 0) for b in books])
bot_count = Sum([If(shelf[b] == 0, 1, 0) for b in books])

solver.add(top_count >= 2)
solver.add(mid_count >= 2)
solver.add(bot_count >= 2)

# Constraint 2: More books on bottom than top
solver.add(bot_count > top_count)

# Constraint 3: I is on the middle shelf
solver.add(shelf['I'] == 1)

# Constraint 4: K is on a higher shelf than F
solver.add(shelf['K'] > shelf['F'])

# Constraint 5: O is on a higher shelf than L
solver.add(shelf['O'] > shelf['L'])

# Constraint 6: F is on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# Now evaluate each option to see which MUST be true
# An option MUST be true if adding its negation makes the problem unsat

# Option A: O is on a shelf higher than M => shelf['O'] > shelf['M']
opt_a_constr = shelf['O'] > shelf['M']

# Option B: K is on a shelf higher than G => shelf['K'] > shelf['G']
opt_b_constr = shelf['K'] > shelf['G']

# Option C: I is on a shelf higher than F => shelf['I'] > shelf['F']
# I is on middle (1), so this means F is on bottom (0)
opt_c_constr = shelf['I'] > shelf['F']

# Option D: G is on a shelf higher than O => shelf['G'] > shelf['O']
opt_d_constr = shelf['G'] > shelf['O']

# Option E: F is on a shelf higher than L => shelf['F'] > shelf['L']
opt_e_constr = shelf['F'] > shelf['L']

# For each option, we want to know if it MUST be true.
# "Must be true" means the negation makes the problem unsat.
# So let's check: is negating the option compatible with the constraints?

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        # Adding the negation makes it unsat, so the original must be true
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