from z3 import *

# Books: F, G, H, I, K, L, M, O
# Shelves: top=2, middle=1, bottom=0 (higher number = higher shelf)
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(f'shelf_{b}') for b in books}

# Base constraints
base = []
for b in books:
    base.append(Or(shelf[b] == 0, shelf[b] == 1, shelf[b] == 2))

# At least 2 books on each shelf
for s in [0, 1, 2]:
    base.append(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)

# More books on bottom shelf (0) than top shelf (2)
base.append(Sum([If(shelf[b] == 0, 1, 0) for b in books]) > Sum([If(shelf[b] == 2, 1, 0) for b in books]))

# I is on the middle shelf
base.append(shelf['I'] == 1)

# K is on a higher shelf than F
base.append(shelf['K'] > shelf['F'])

# O is on a higher shelf than L
base.append(shelf['O'] > shelf['L'])

# F is on the same shelf as M
base.append(shelf['F'] == shelf['M'])

# Answer options (what each claims):
# (A) O is placed on a shelf higher than the shelf M is placed on.
opt_a = shelf['O'] > shelf['M']
# (B) K is placed on a shelf higher than the shelf G is placed on.
opt_b = shelf['K'] > shelf['G']
# (C) I is placed on a shelf higher than the shelf F is placed on.
opt_c = shelf['I'] > shelf['F']
# (D) G is placed on a shelf higher than the shelf O is placed on.
opt_d = shelf['G'] > shelf['O']
# (E) F is placed on a shelf higher than the shelf L is placed on.
opt_e = shelf['F'] > shelf['L']

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

# For "must be true": check if negation is UNSAT
must_be_true = []
for letter, opt in options:
    s = Solver()
    s.add(base)
    s.add(Not(opt))  # Try to find a valid arrangement where the option is FALSE
    result = s.check()
    if result == unsat:
        must_be_true.append(letter)
        print(f"Option {letter}: MUST BE TRUE (negation is UNSAT)")
    elif result == sat:
        print(f"Option {letter}: NOT necessarily true (counterexample exists)")
        m = s.model()
        for b in books:
            val = m[shelf[b]]
            shelf_name = {0: "bottom", 1: "middle", 2: "top"}[int(str(val))]
            print(f"  {b} -> {shelf_name}")
    else:
        print(f"Option {letter}: UNKNOWN")

print()
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")