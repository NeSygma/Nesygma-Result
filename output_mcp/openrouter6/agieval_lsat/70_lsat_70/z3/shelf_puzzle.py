from z3 import *

# BENCHMARK_MODE = True  # According to configuration

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
opt_a_constr = (F == G)
opt_b_constr = (G == H)
opt_c_constr = (H == M)
opt_d_constr = (I == G)
opt_e_constr = (K == O)

# Evaluate each option using the exact skeleton
found_options = []
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