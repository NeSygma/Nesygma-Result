from z3 import *

# Shelves: top=0, middle=1, bottom=2
# "Higher shelf" = lower number

books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(f'shelf_{b}') for b in books}

def add_base_constraints(solver):
    # Each book on shelf 0, 1, or 2
    for b in books:
        solver.add(Or(shelf[b] == 0, shelf[b] == 1, shelf[b] == 2))
    
    # At least 2 books on each shelf
    for s in range(3):
        solver.add(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)
    
    # More books on bottom shelf than top shelf
    solver.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) > Sum([If(shelf[b] == 0, 1, 0) for b in books]))
    
    # I is on the middle shelf
    solver.add(shelf['I'] == 1)
    
    # K is on a higher shelf than F
    solver.add(shelf['K'] < shelf['F'])
    
    # O is on a higher shelf than L
    solver.add(shelf['O'] < shelf['L'])
    
    # F is on the same shelf as M
    solver.add(shelf['F'] == shelf['M'])

# Option constraints
opt_constrs = {
    "A": shelf['I'] == shelf['M'],       # I and M same shelf
    "B": shelf['K'] == shelf['G'],       # K and G same shelf
    "C": shelf['L'] == shelf['F'],       # L and F same shelf
    "D": shelf['M'] == shelf['H'],       # M and H same shelf
    "E": shelf['H'] == shelf['O'],       # H and O same shelf
}

decision_vars = [shelf[b] for b in books]

found_options = []

for letter, constr in opt_constrs.items():
    s = Solver()
    add_base_constraints(s)
    s.add(constr)
    
    if s.check() == sat:
        # Found one solution; check if there's another
        m1 = s.model()
        # Block this specific model
        block = Or([v != m1.eval(v, model_completion=True) for v in decision_vars])
        s.add(block)
        if s.check() != sat:
            # Only one solution exists -> fully determined
            found_options.append(letter)
        # else: multiple solutions, not fully determined

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")