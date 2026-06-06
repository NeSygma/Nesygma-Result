from z3 import *

books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(f'shelf_{b}') for b in books}

def base_constraints(s):
    # domain
    for b in books:
        s.add(shelf[b] >= 0, shelf[b] <= 2)
    # I on middle
    s.add(shelf['I'] == 1)
    # K higher than F
    s.add(shelf['K'] < shelf['F'])
    # O higher than L
    s.add(shelf['O'] < shelf['L'])
    # F same shelf as M
    s.add(shelf['F'] == shelf['M'])
    # at least 2 on each shelf
    s.add(Sum([If(shelf[b] == 0, 1, 0) for b in books]) >= 2)
    s.add(Sum([If(shelf[b] == 1, 1, 0) for b in books]) >= 2)
    s.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) >= 2)
    # more on bottom than top
    s.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) > Sum([If(shelf[b] == 0, 1, 0) for b in books]))

# Option constraints
options = {
    "A": shelf['I'] == shelf['M'],  # I and M same shelf (I already 1, so M=1)
    "B": shelf['K'] == shelf['G'],
    "C": shelf['L'] == shelf['F'],
    "D": shelf['M'] == shelf['H'],
    "E": shelf['H'] == shelf['O']
}

unique_options = []

for letter, constr in options.items():
    s = Solver()
    base_constraints(s)
    s.add(constr)
    # First check if satisfiable
    if s.check() == sat:
        m = s.model()
        # Try to find a second distinct solution
        # Block the current assignment: at least one book different shelf
        blocking = []
        for b in books:
            blocking.append(shelf[b] != m.eval(shelf[b], model_completion=True))
        s.add(Or(blocking))
        if s.check() == unsat:
            # Unique solution
            unique_options.append(letter)
        # else: multiple solutions, not fully determined
    # else: unsat, option not possible

if len(unique_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unique_options[0]}")
elif len(unique_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {unique_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")