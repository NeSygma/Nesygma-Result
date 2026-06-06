from z3 import *

# Shelves: 0 = top, 1 = middle, 2 = bottom
solver = Solver()

books = ["F", "G", "H", "I", "K", "L", "M", "O"]
shelf = {b: Int(f"shelf_{b}") for b in books}

# Each book is on one of the three shelves
for b in books:
    solver.add(And(shelf[b] >= 0, shelf[b] <= 2))

# At least two books on each shelf
solver.add(Sum([If(shelf[b] == 0, 1, 0) for b in books]) >= 2)
solver.add(Sum([If(shelf[b] == 1, 1, 0) for b in books]) >= 2)
solver.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) >= 2)

# More books on bottom shelf than top shelf
solver.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) > Sum([If(shelf[b] == 0, 1, 0) for b in books]))

# I is on the middle shelf
solver.add(shelf["I"] == 1)

# K is on a higher shelf than F (higher = smaller number)
solver.add(shelf["K"] < shelf["F"])

# O is on a higher shelf than L
solver.add(shelf["O"] < shelf["L"])

# F is on the same shelf as M
solver.add(shelf["F"] == shelf["M"])

# Now evaluate each option

options = {
    "A": ["F", "M"],
    "B": ["F", "H", "M"],
    "C": ["G", "H", "K"],
    "D": ["F", "G", "M", "O"],
    "E": ["G", "H", "L", "M"]
}

found_options = []

for letter, opt_books in options.items():
    solver.push()
    # The bottom shelf (shelf == 2) must contain exactly these books
    for b in books:
        if b in opt_books:
            solver.add(shelf[b] == 2)  # This book IS on bottom shelf
        else:
            solver.add(shelf[b] != 2)  # This book is NOT on bottom shelf
    if solver.check() == sat:
        found_options.append(letter)
        # Print model details for debug
        m = solver.model()
        print(f"Option {letter}: SAT - Model:")
        for b in books:
            sh = m.eval(shelf[b])
            shelf_name = {0: "top", 1: "middle", 2: "bottom"}
            print(f"  {b}: {shelf_name[int(str(sh))]}")
    else:
        print(f"Option {letter}: UNSAT")
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