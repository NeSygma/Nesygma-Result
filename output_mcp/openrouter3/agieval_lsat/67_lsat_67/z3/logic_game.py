from z3 import *

# Declare shelf variables for each book
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(f'shelf_{b}') for b in books}

solver = Solver()

# Base constraints
# 1. Each shelf has at least two books
for s in range(3):  # 0=top, 1=middle, 2=bottom
    count = Sum([If(shelf[b] == s, 1, 0) for b in books])
    solver.add(count >= 2)

# 2. More books on bottom shelf than top shelf
count_top = Sum([If(shelf[b] == 0, 1, 0) for b in books])
count_bottom = Sum([If(shelf[b] == 2, 1, 0) for b in books])
solver.add(count_bottom > count_top)

# 3. I is on middle shelf
solver.add(shelf['I'] == 1)

# 4. K is on a higher shelf than F (higher means smaller number)
solver.add(shelf['K'] < shelf['F'])

# 5. O is on a higher shelf than L
solver.add(shelf['O'] < shelf['L'])

# 6. F and M are on the same shelf
solver.add(shelf['F'] == shelf['M'])

# Domain constraints: each shelf is 0,1,2
for b in books:
    solver.add(shelf[b] >= 0, shelf[b] <= 2)

# Now test each option
found_options = []

# Option A: I and M are on the same shelf
opt_a_constr = (shelf['I'] == shelf['M'])
# Option B: K and G are on the same shelf
opt_b_constr = (shelf['K'] == shelf['G'])
# Option C: L and F are on the same shelf
opt_c_constr = (shelf['L'] == shelf['F'])
# Option D: M and H are on the same shelf
opt_d_constr = (shelf['M'] == shelf['H'])
# Option E: H and O are on the same shelf
opt_e_constr = (shelf['H'] == shelf['O'])

for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
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