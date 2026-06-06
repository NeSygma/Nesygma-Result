from z3 import *

# Books: F, G, H, I, K, L, M, O
# Shelves: 0 = top, 1 = middle, 2 = bottom
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(f'shelf_{b}') for b in books}

solver = Solver()

# Each book is on exactly one shelf: 0 (top), 1 (middle), 2 (bottom)
for b in books:
    solver.add(Or([shelf[b] == i for i in [0, 1, 2]]))

# At least two books on each shelf
for s in [0, 1, 2]:
    solver.add(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)

# More books on bottom shelf than top shelf
solver.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) > Sum([If(shelf[b] == 0, 1, 0) for b in books]))

# I is on middle shelf
solver.add(shelf['I'] == 1)

# K is on a higher shelf than F (higher = smaller number)
solver.add(shelf['K'] < shelf['F'])

# O is on a higher shelf than L
solver.add(shelf['O'] < shelf['L'])

# F is on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# Now test each option: does adding that condition make the entire assignment fully determined?
# "Fully determined" means there is exactly one possible assignment for all 8 books.
# We test by checking if the system has exactly one solution.

def count_solutions(solver):
    """Count solutions by blocking each found solution."""
    count = 0
    while solver.check() == sat:
        count += 1
        if count > 1:
            break
        m = solver.model()
        # Block this solution
        solver.add(Or([shelf[b] != m.eval(shelf[b], model_completion=True) for b in books]))
    return count

found_options = []

for letter, extra_constr in [
    ("A", shelf['I'] == shelf['M']),
    ("B", shelf['K'] == shelf['G']),
    ("C", shelf['L'] == shelf['F']),
    ("D", shelf['M'] == shelf['H']),
    ("E", shelf['H'] == shelf['O'])
]:
    solver.push()
    solver.add(extra_constr)
    # Check if satisfiable first
    if solver.check() == sat:
        # Now count solutions
        # We need a fresh copy for counting
        s_copy = Solver()
        for c in solver.assertions():
            s_copy.add(c)
        n = count_solutions(s_copy)
        if n == 1:
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