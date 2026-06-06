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
solver.add(Sum([If(shelf[b] == 0, 1, 0) for b in books]) >= 2)
solver.add(Sum([If(shelf[b] == 1, 1, 0) for b in books]) >= 2)
solver.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) >= 2)

# More books on bottom shelf than top shelf
solver.add(Sum([If(shelf[b] == 2, 1, 0) for b in books]) > Sum([If(shelf[b] == 0, 1, 0) for b in books]))

# I is placed on the middle shelf
solver.add(shelf['I'] == 1)

# K is placed on a higher shelf than F (higher = smaller number)
solver.add(shelf['K'] < shelf['F'])

# O is placed on a higher shelf than L
solver.add(shelf['O'] < shelf['L'])

# F is placed on the same shelf as M
solver.add(shelf['F'] == shelf['M'])

# Let's first check if the base constraints are satisfiable
print("Base constraints check:")
result = solver.check()
print(f"Result: {result}")
if result == sat:
    m = solver.model()
    for b in books:
        print(f"  {b}: shelf {m[shelf[b]]}")
    
    # Count per shelf
    top = sum(1 for b in books if m[shelf[b]].as_long() == 0)
    mid = sum(1 for b in books if m[shelf[b]].as_long() == 1)
    bot = sum(1 for b in books if m[shelf[b]].as_long() == 2)
    print(f"  Top: {top}, Middle: {mid}, Bottom: {bot}")

# Now let's think about what MUST be true.
# We need to check each option: is it forced by the constraints?
# An option "must be true" if adding its NEGATION makes the constraints unsatisfiable.

print("\n--- Testing which options MUST be true ---")

# Option A: O < M (O higher than M)
solver.push()
solver.add(Not(shelf['O'] < shelf['M']))  # O >= M
res_a = solver.check()
print(f"A negation (O >= M): {res_a}")
solver.pop()

# Option B: K < G (K higher than G)
solver.push()
solver.add(Not(shelf['K'] < shelf['G']))  # K >= G
res_b = solver.check()
print(f"B negation (K >= G): {res_b}")
solver.pop()

# Option C: I < F (I higher than F, i.e., F on bottom since I=1)
solver.push()
solver.add(Not(shelf['I'] < shelf['F']))  # I >= F
res_c = solver.check()
print(f"C negation (I >= F): {res_c}")
solver.pop()

# Option D: G < O (G higher than O)
solver.push()
solver.add(Not(shelf['G'] < shelf['O']))  # G >= O
res_d = solver.check()
print(f"D negation (G >= O): {res_d}")
solver.pop()

# Option E: F < L (F higher than L)
solver.push()
solver.add(Not(shelf['F'] < shelf['L']))  # F >= L
res_e = solver.check()
print(f"E negation (F >= L): {res_e}")
solver.pop()