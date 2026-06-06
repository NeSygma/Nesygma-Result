from z3 import *

# -------------------------------------------------
# Base model (common to all options)
# -------------------------------------------------
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(f"shelf_{b}") for b in books}

solver = Solver()

# Domain: each book is on one of the three shelves (1=bottom, 2=middle, 3=top)
for b in books:
    solver.add(shelf[b] >= 1, shelf[b] <= 3)

# At least two books on each shelf
for s in (1, 2, 3):
    solver.add(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)

# More books on bottom than on top
bottom_cnt = Sum([If(shelf[b] == 1, 1, 0) for b in books])
top_cnt    = Sum([If(shelf[b] == 3, 1, 0) for b in books])
solver.add(bottom_cnt > top_cnt)

# Specific constraints from the problem
solver.add(shelf['I'] == 2)          # I is on the middle shelf
solver.add(shelf['K'] > shelf['F'])  # K higher than F
solver.add(shelf['O'] > shelf['L'])  # O higher than L
solver.add(shelf['F'] == shelf['M'])# F same shelf as M
solver.add(shelf['G'] == 3)          # G is on the top shelf (hypothesis)

# -------------------------------------------------
# Option‑specific constraints
# -------------------------------------------------
options = {
    "A": {"H", "I"},
    "B": {"I", "L"},
    "C": {"H", "I", "L"},
    "D": {"I", "K", "L"},
    "E": {"F", "I", "M"},
}

found_options = []

for letter, mids in options.items():
    solver.push()
    # enforce that exactly the books in mids are on the middle shelf
    for b in books:
        if b in mids:
            solver.add(shelf[b] == 2)
        else:
            solver.add(shelf[b] != 2)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# -------------------------------------------------
# Output according to the required skeleton
# -------------------------------------------------
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")