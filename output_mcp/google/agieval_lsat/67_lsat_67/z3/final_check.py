from z3 import *

books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(f'shelf_{b}') for b in books}

# Mapping: Top=2, Middle=1, Bottom=0
# "More of the books are placed on the bottom shelf than the top shelf."
# Bottom(0) > Top(2)
# "K is placed on a higher shelf than F."
# K > F
# "O is placed on a higher shelf than L."
# O > L

base_constraints = []
for b in books:
    base_constraints.append(shelf[b] >= 0)
    base_constraints.append(shelf[b] <= 2)

for s in range(3):
    base_constraints.append(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)

base_constraints.append(Sum([If(shelf[b] == 0, 1, 0) for b in books]) > Sum([If(shelf[b] == 2, 1, 0) for b in books]))
base_constraints.append(shelf['I'] == 1)
base_constraints.append(shelf['K'] > shelf['F'])
base_constraints.append(shelf['O'] > shelf['L'])
base_constraints.append(shelf['F'] == shelf['M'])

solver = Solver()
solver.add(base_constraints)

found_options = []
for letter, constr in [("A", shelf['I'] == shelf['M']), ("B", shelf['K'] == shelf['G']), ("C", shelf['L'] == shelf['F']), ("D", shelf['M'] == shelf['H']), ("E", shelf['H'] == shelf['O'])]:
    solver.push()
    solver.add(constr)
    
    # Check if this option fully determines the placement
    # A placement is fully determined if there is only 1 solution
    count = 0
    s_inner = Solver()
    s_inner.add(base_constraints)
    s_inner.add(constr)
    while s_inner.check() == sat:
        count += 1
        m = s_inner.model()
        s_inner.add(Or([shelf[b] != m[shelf[b]] for b in books]))
    
    if count == 1:
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