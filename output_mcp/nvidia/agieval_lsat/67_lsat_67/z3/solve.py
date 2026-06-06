from z3 import *

books = ['F','G','H','I','K','L','M','O']
shelf = {b: Int(f'shelf_{b}') for b in books}

# Base constraints
count_top = Sum([If(shelf[b] == 0, 1, 0) for b in books])
count_mid = Sum([If(shelf[b] == 1, 1, 0) for b in books])
count_bot = Sum([If(shelf[b] == 2, 1, 0) for b in books])

base_constraints = [
    count_top >= 2,
    count_mid >= 2,
    count_bot >= 2,
    count_bot > count_top,
    shelf['I'] == 1,
    shelf['K'] < shelf['F'],
    shelf['O'] < shelf['L']
]

# Option constraints
opt_a_constr = shelf['I'] == shelf['M']
opt_b_constr = shelf['K'] == shelf['G']
opt_c_constr = shelf['L'] == shelf['F']
opt_d_constr = shelf['M'] == shelf['H']
opt_e_constr = shelf['H'] == shelf['O']

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    s = Solver()
    # add base constraints
    for bc in base_constraints:
        s.add(bc)
    # add option constraint
    s.add(constr)
    # check
    result = s.check()
    if result == sat:
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