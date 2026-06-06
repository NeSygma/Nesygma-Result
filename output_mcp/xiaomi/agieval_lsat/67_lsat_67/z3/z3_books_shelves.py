from z3 import *

# Shelves: 0 = top, 1 = middle, 2 = bottom
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(f'shelf_{b}') for b in books}

solver = Solver()

# Each book on shelf 0, 1, or 2
for b in books:
    solver.add(Or(shelf[b] == 0, shelf[b] == 1, shelf[b] == 2))

# At least two books on each shelf
for s in range(3):
    solver.add(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)

# More books on bottom shelf than top shelf
solver.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) > Sum([If(shelf[b] == 0, 1, 0) for b in books]))

# I is placed on the middle shelf
solver.add(shelf['I'] == 1)

# K is placed on a higher shelf than F (higher = smaller number: top=0 > middle=1 > bottom=2)
solver.add(shelf['K'] < shelf['F'])

# O is placed on a higher shelf than L
solver.add(shelf['O'] < shelf['L'])

# F is placed on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# Now test each option to see which one fully determines the placement
# An option "fully determines" if adding it makes the solution unique

def get_all_solutions(extra_constraints):
    """Find all solutions given extra constraints"""
    s = Solver()
    # Copy base constraints
    for b in books:
        s.add(Or(shelf[b] == 0, shelf[b] == 1, shelf[b] == 2))
    for sh in range(3):
        s.add(Sum([If(shelf[b] == sh, 1, 0) for b in books]) >= 2)
    s.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) > Sum([If(shelf[b] == 0, 1, 0) for b in books]))
    s.add(shelf['I'] == 1)
    s.add(shelf['K'] < shelf['F'])
    s.add(shelf['O'] < shelf['L'])
    s.add(shelf['F'] == shelf['M'])
    for c in extra_constraints:
        s.add(c)
    
    solutions = []
    decision_vars = [shelf[b] for b in books]
    while s.check() == sat:
        m = s.model()
        sol = tuple(m.eval(v, model_completion=True).as_long() for v in decision_vars)
        solutions.append(sol)
        s.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))
    return solutions

# Option constraints
opt_constrs = {
    "A": [shelf['I'] == shelf['M']],       # I and M same shelf
    "B": [shelf['K'] == shelf['G']],       # K and G same shelf
    "C": [shelf['L'] == shelf['F']],       # L and F same shelf
    "D": [shelf['M'] == shelf['H']],       # M and H same shelf
    "E": [shelf['H'] == shelf['O']],       # H and O same shelf
}

found_options = []
for letter, constr in opt_constrs.items():
    solutions = get_all_solutions(constr)
    if len(solutions) == 1:
        found_options.append(letter)
        print(f"Option {letter}: UNIQUE solution = {solutions[0]}")
    else:
        print(f"Option {letter}: {len(solutions)} solutions (not unique)")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")