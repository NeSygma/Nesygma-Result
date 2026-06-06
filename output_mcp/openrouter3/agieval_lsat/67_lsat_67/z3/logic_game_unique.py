from z3 import *

# Declare shelf variables for each book
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(f'shelf_{b}') for b in books}

# Base constraints
base_solver = Solver()
for s in range(3):
    count = Sum([If(shelf[b] == s, 1, 0) for b in books])
    base_solver.add(count >= 2)

count_top = Sum([If(shelf[b] == 0, 1, 0) for b in books])
count_bottom = Sum([If(shelf[b] == 2, 1, 0) for b in books])
base_solver.add(count_bottom > count_top)

base_solver.add(shelf['I'] == 1)
base_solver.add(shelf['K'] < shelf['F'])
base_solver.add(shelf['O'] < shelf['L'])
base_solver.add(shelf['F'] == shelf['M'])

for b in books:
    base_solver.add(shelf[b] >= 0, shelf[b] <= 2)

# Options
options = {
    'A': shelf['I'] == shelf['M'],
    'B': shelf['K'] == shelf['G'],
    'C': shelf['L'] == shelf['F'],
    'D': shelf['M'] == shelf['H'],
    'E': shelf['H'] == shelf['O']
}

found_options = []

for letter, constr in options.items():
    # Create a new solver for this option
    s = Solver()
    s.add(base_solver.assertions())
    s.add(constr)
    
    # Check if satisfiable
    if s.check() != sat:
        continue
    
    # Find first model
    m1 = s.model()
    # Create a blocking clause to find a second model
    blocking = Or([shelf[b] != m1[shelf[b]] for b in books])
    s.add(blocking)
    
    # Check if a second model exists
    if s.check() == sat:
        # More than one solution
        continue
    else:
        # Exactly one solution
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")