from z3 import *

# Exactly eight books: F, G, H, I, K, L, M, O
# Three shelves: top (0), middle (1), bottom (2)
# Higher shelf = smaller number (top=0 is highest, bottom=2 is lowest)

solver = Solver()

# Variables: shelf assignment for each book (0=top, 1=middle, 2=bottom)
books = ['F', 'G', 'H', 'I', 'K', 'L', 'M', 'O']
shelf = {b: Int(f'shelf_{b}') for b in books}

# Domain: each shelf is 0, 1, or 2
for b in books:
    solver.add(shelf[b] >= 0, shelf[b] <= 2)

# At least two books on each shelf
for s in range(3):
    solver.add(Sum([If(shelf[b] == s, 1, 0) for b in books]) >= 2)

# More books on bottom shelf (2) than top shelf (0)
solver.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) > 
           Sum([If(shelf[b] == 0, 1, 0) for b in books]))

# I is on the middle shelf (1)
solver.add(shelf['I'] == 1)

# K is on a higher shelf than F (higher = smaller number)
solver.add(shelf['K'] < shelf['F'])

# O is on a higher shelf than L
solver.add(shelf['O'] < shelf['L'])

# F is on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# Additional condition from the question: L is on a higher shelf than H
solver.add(shelf['L'] < shelf['H'])

# Let's first check if the base constraints are satisfiable
print("Checking base constraints...")
result = solver.check()
if result == sat:
    m = solver.model()
    print("SAT - found a model:")
    for b in books:
        print(f"  {b}: shelf {m[shelf[b]]}")
else:
    print(f"UNSAT - base constraints are inconsistent")
    exit()

# Now we need to find which option MUST be true.
# An option "must be true" if in EVERY valid model, it holds.
# So we check: is there a model where the option is FALSE?
# If no model exists where the option is false, then it must be true.

print("\nChecking which options MUST be true...")
must_be_true = []
for letter in ["A", "B", "C", "D", "E"]:
    solver.push()
    if letter == "A":
        # A: F and G on same shelf. Check if NOT(F and G same shelf) is possible
        solver.add(shelf['F'] != shelf['G'])
    elif letter == "B":
        solver.add(shelf['G'] != shelf['H'])
    elif letter == "C":
        solver.add(shelf['H'] != shelf['M'])
    elif letter == "D":
        solver.add(shelf['I'] != shelf['G'])
    elif letter == "E":
        solver.add(shelf['K'] != shelf['O'])
    
    if solver.check() == unsat:
        # No model where this option is false -> it MUST be true
        must_be_true.append(letter)
    solver.pop()

print(f"Options that MUST be true: {must_be_true}")

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")