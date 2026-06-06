from z3 import *

# Books
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(f'shelf_{b}') for b in books}

solver = Solver()

# Base constraints
for b in books:
    solver.add(shelf[b] >= 0, shelf[b] <= 2)

solver.add(shelf['I'] == 1)  # I on middle shelf
solver.add(shelf['F'] == shelf['M'])  # F and M same shelf
solver.add(shelf['K'] < shelf['F'])  # K higher than F
solver.add(shelf['O'] < shelf['L'])  # O higher than L

# At least two books per shelf
for s in range(3):
    solver.add(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)

# Bottom shelf count > top shelf count
top_count = Sum([If(shelf[b] == 0, 1, 0) for b in books])
bottom_count = Sum([If(shelf[b] == 2, 1, 0) for b in books])
solver.add(bottom_count > top_count)

# Option constraints
opt_a_constr = (shelf['I'] == shelf['M'])
opt_b_constr = (shelf['K'] == shelf['G'])
opt_c_constr = (shelf['L'] == shelf['F'])
opt_d_constr = (shelf['M'] == shelf['H'])
opt_e_constr = (shelf['H'] == shelf['O'])

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        # Count solutions
        count = 0
        while solver.check() == sat:
            count += 1
            m = solver.model()
            # Blocking clause to find next solution
            solver.add(Or([shelf[b] != m[shelf[b]] for b in books]))
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