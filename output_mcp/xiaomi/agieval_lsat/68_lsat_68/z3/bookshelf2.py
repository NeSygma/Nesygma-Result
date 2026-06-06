from z3 import *

# Books: F, G, H, I, K, L, M, O
# Shelves: 0 = top, 1 = middle, 2 = bottom
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']

def make_base():
    solver = Solver()
    shelf = {b: Int(f'shelf_{b}') for b in books}
    for b in books:
        solver.add(Or(shelf[b] == 0, shelf[b] == 1, shelf[b] == 2))
    for s in range(3):
        solver.add(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)
    solver.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) > Sum([If(shelf[b] == 0, 1, 0) for b in books]))
    solver.add(shelf['I'] == 1)
    solver.add(shelf['K'] < shelf['F'])
    solver.add(shelf['O'] < shelf['L'])
    solver.add(shelf['F'] == shelf['M'])
    return solver, shelf

# Define option constraints
options = {
    "A": lambda s: s['O'] < s['M'],   # O higher than M
    "B": lambda s: s['K'] < s['G'],   # K higher than G
    "C": lambda s: s['I'] < s['F'],   # I higher than F
    "D": lambda s: s['G'] < s['O'],   # G higher than O
    "E": lambda s: s['F'] < s['L'],   # F higher than L
}

# For each option, check if it MUST be true (i.e., negation is unsat)
must_be_true = []
for letter, constr_fn in options.items():
    solver, shelf = make_base()
    # Add negation of the option
    solver.add(Not(constr_fn(shelf)))
    result = solver.check()
    if result == unsat:
        must_be_true.append(letter)
        print(f"Option {letter}: MUST be true (negation is unsat)")
    elif result == sat:
        print(f"Option {letter}: NOT necessarily true (counterexample exists)")
        m = solver.model()
        for b in books:
            print(f"  shelf[{b}] = {m[shelf[b]]}")
    else:
        print(f"Option {letter}: unknown")

print()
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-true options found {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-true options found")