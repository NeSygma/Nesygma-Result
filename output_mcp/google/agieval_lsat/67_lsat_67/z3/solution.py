from z3 import *

def count_solutions(base_constraints, additional_constraint):
    solver = Solver()
    solver.add(base_constraints)
    solver.add(additional_constraint)
    
    solutions = []
    while solver.check() == sat:
        m = solver.model()
        sol = {b: m[shelf[b]] for b in books}
        solutions.append(sol)
        # Block this solution
        solver.add(Or([shelf[b] != m[shelf[b]] for b in books]))
    return len(solutions)

books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(f'shelf_{b}') for b in books}

base_constraints = []
# Shelves: 0=Top, 1=Middle, 2=Bottom
for b in books:
    base_constraints.append(shelf[b] >= 0)
    base_constraints.append(shelf[b] <= 2)

# At least two books on each shelf
for s in range(3):
    base_constraints.append(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)

# More books on bottom than top
base_constraints.append(Sum([If(shelf[b] == 2, 1, 0) for b in books]) > Sum([If(shelf[b] == 0, 1, 0) for b in books]))

# I is on middle
base_constraints.append(shelf['I'] == 1)

# K higher than F
base_constraints.append(shelf['K'] > shelf['F'])

# O higher than L
base_constraints.append(shelf['O'] > shelf['L'])

# F and M same shelf
base_constraints.append(shelf['F'] == shelf['M'])

options = {
    "A": shelf['I'] == shelf['M'],
    "B": shelf['K'] == shelf['G'],
    "C": shelf['L'] == shelf['F'],
    "D": shelf['M'] == shelf['H'],
    "E": shelf['H'] == shelf['O']
}

found_options = []
for letter, constr in options.items():
    if count_solutions(base_constraints, constr) == 1:
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