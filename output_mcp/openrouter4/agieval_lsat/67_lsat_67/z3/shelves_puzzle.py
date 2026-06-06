from z3 import *

# Books
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']

# Shelf variables: 0 = top, 1 = middle, 2 = bottom
shelf = {b: Int(f'shelf_{b}') for b in books}

def make_base_solver():
    solver = Solver()
    # Domain: shelves 0,1,2
    for b in books:
        solver.add(shelf[b] >= 0, shelf[b] <= 2)
    
    # At least 2 books per shelf
    for s in range(3):
        solver.add(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)
    
    # More books on bottom (2) than top (0)
    bottom_count = Sum([If(shelf[b] == 2, 1, 0) for b in books])
    top_count = Sum([If(shelf[b] == 0, 1, 0) for b in books])
    solver.add(bottom_count > top_count)
    
    # I is on middle shelf (1)
    solver.add(shelf['I'] == 1)
    
    # K is on a higher shelf than F (higher = smaller number)
    solver.add(shelf['K'] < shelf['F'])
    
    # O is on a higher shelf than L
    solver.add(shelf['O'] < shelf['L'])
    
    # F is on same shelf as M
    solver.add(shelf['F'] == shelf['M'])
    
    return solver

# Define option constraints
options = [
    ("A", shelf['I'] == shelf['M']),
    ("B", shelf['K'] == shelf['G']),
    ("C", shelf['L'] == shelf['F']),
    ("D", shelf['M'] == shelf['H']),
    ("E", shelf['H'] == shelf['O'])
]

results = {}

for letter, constr in options:
    solver = make_base_solver()
    solver.add(constr)
    
    decision_vars = [shelf[b] for b in books]
    solution_count = 0
    
    while solver.check() == sat:
        m = solver.model()
        solution_count += 1
        # Block this solution
        solver.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))
    
    results[letter] = solution_count
    print(f"Option {letter}: {solution_count} solutions")

# Find the option with exactly 1 solution
found = [l for l, cnt in results.items() if cnt == 1]

if len(found) == 1:
    print("STATUS: sat")
    print(f"answer:{found[0]}")
elif len(found) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")