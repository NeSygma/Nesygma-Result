from z3 import *

# Declare shelf variables for each book
F = Int('F')
G = Int('G')
H = Int('H')
I = Int('I')
K = Int('K')
L = Int('L')
M = Int('M')
O = Int('O')

# All shelf variables for counting
all_shelves = [F, G, H, I, K, L, M, O]

solver = Solver()

# 1. Each shelf has at least two books
top_count = Sum([If(s == 1, 1, 0) for s in all_shelves])
middle_count = Sum([If(s == 2, 1, 0) for s in all_shelves])
bottom_count = Sum([If(s == 3, 1, 0) for s in all_shelves])

solver.add(top_count >= 2)
solver.add(middle_count >= 2)
solver.add(bottom_count >= 2)

# 2. More books on bottom than top
solver.add(bottom_count > top_count)

# 3. I is on middle shelf
solver.add(I == 2)

# 4. K is on a higher shelf than F (higher means smaller number)
solver.add(K < F)

# 5. O is on a higher shelf than L
solver.add(O < L)

# 6. F and M on same shelf
solver.add(F == M)

# Additional condition for the question: L is placed on a shelf higher than H
solver.add(L < H)

# Ensure all shelves are within 1..3
for s in all_shelves:
    solver.add(s >= 1, s <= 3)

# Define option constraints
opt_a = (F == G)
opt_b = (G == H)
opt_c = (H == M)
opt_d = (I == G)
opt_e = (K == O)

# For each option, check if its negation is unsatisfiable
options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

must_true = []
for letter, opt in options:
    s = Solver()
    s.add(solver.assertions())  # copy base constraints
    s.add(Not(opt))
    res = s.check()
    if res == unsat:
        must_true.append(letter)

print(f"Must-true options: {must_true}")
if len(must_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_true[0]}")
elif len(must_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-true options found {must_true}")
else:
    print("STATUS: unsat")
    print("Refine: No must-true options found")