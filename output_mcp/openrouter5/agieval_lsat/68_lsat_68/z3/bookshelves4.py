from z3 import *

# Exactly eight books: F, G, H, I, K, L, M, O
# Three shelves: top (0), middle (1), bottom (2)
# Higher shelf = smaller number (top=0 is highest, bottom=2 is lowest)

solver = Solver()

# Variables: shelf assignment for each book (0=top, 1=middle, 2=bottom)
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(f'shelf_{b}') for b in books}

# Domain: each shelf is 0, 1, or 2
for b in books:
    solver.add(shelf[b] >= 0, shelf[b] <= 2)

# At least two books on each shelf
solver.add(Sum([If(shelf[b] == 0, 1, 0) for b in books]) >= 2)
solver.add(Sum([If(shelf[b] == 1, 1, 0) for b in books]) >= 2)
solver.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) >= 2)

# More books on bottom shelf than top shelf
solver.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) > Sum([If(shelf[b] == 0, 1, 0) for b in books]))

# I is placed on the middle shelf
solver.add(shelf['I'] == 1)

# K is placed on a higher shelf than F (higher = smaller number)
solver.add(shelf['K'] < shelf['F'])

# O is placed on a higher shelf than L
solver.add(shelf['O'] < shelf['L'])

# F is placed on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# Let's first check if the base constraints are satisfiable
print("Checking base constraints...")
if solver.check() == sat:
    m = solver.model()
    for b in books:
        print(f"{b}: shelf {m[shelf[b]]}")
else:
    print("Base constraints are UNSAT!")
    exit()

# Now the problem asks "which must be true" - this is a validity/entailment question.
# An option "must be true" if it holds in ALL valid models.
# So we need to check if the negation of each option is UNSAT (i.e., the option is forced).

# Let's check each option by seeing if its negation is consistent with the premises.
# If the negation is UNSAT, the option MUST be true.

found_options = []
for letter, constr in [("A", shelf['O'] < shelf['M']), 
                        ("B", shelf['K'] < shelf['G']), 
                        ("C", shelf['I'] < shelf['F']), 
                        ("D", shelf['G'] < shelf['O']), 
                        ("E", shelf['F'] < shelf['L'])]:
    solver.push()
    # Add the NEGATION of the option
    solver.add(Not(constr))
    if solver.check() == unsat:
        # Negation is unsat -> option must be true in all models
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