from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for book positions
# 0 = Top, 1 = Middle, 2 = Bottom
F, G, H, I, K, L, M, O = Ints('F G H I K L M O')

# Base constraints
solver = Solver()

# Each book is assigned to a shelf (0, 1, or 2)
for book in [F, G, H, I, K, L, M, O]:
    solver.add(Or(book == 0, book == 1, book == 2))

# At least two books per shelf
shelves = [0, 1, 2]
for shelf in shelves:
    solver.add(Sum([If(book == shelf, 1, 0) for book in [F, G, H, I, K, L, M, O]]) >= 2)

# More books on the bottom shelf (2) than the top shelf (0)
solver.add(Sum([If(book == 2, 1, 0) for book in [F, G, H, I, K, L, M, O]]) > 
           Sum([If(book == 0, 1, 0) for book in [F, G, H, I, K, L, M, O]]))

# I is on the middle shelf (1)
solver.add(I == 1)

# K is on a higher shelf than F (K > F)
solver.add(K > F)

# O is on a higher shelf than L (O > L)
solver.add(O > L)

# F and M are on the same shelf
solver.add(F == M)

# G is on the top shelf (0)
solver.add(G == 0)

# Now evaluate each option
found_options = []

# Option A: H and I are on the middle shelf (1)
opt_a_constr = And(H == 1, I == 1, 
                   Sum([If(book == 1, 1, 0) for book in [F, G, H, I, K, L, M, O]]) == 2)
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: I and L are on the middle shelf (1)
opt_b_constr = And(I == 1, L == 1, 
                   Sum([If(book == 1, 1, 0) for book in [F, G, H, I, K, L, M, O]]) == 2)
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: H, I, and L are on the middle shelf (1)
opt_c_constr = And(H == 1, I == 1, L == 1, 
                   Sum([If(book == 1, 1, 0) for book in [F, G, H, I, K, L, M, O]]) == 3)
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: I, K, and L are on the middle shelf (1)
opt_d_constr = And(I == 1, K == 1, L == 1, 
                   Sum([If(book == 1, 1, 0) for book in [F, G, H, I, K, L, M, O]]) == 3)
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: F, I, and M are on the middle shelf (1)
opt_e_constr = And(F == 1, I == 1, M == 1, 
                   Sum([If(book == 1, 1, 0) for book in [F, G, H, I, K, L, M, O]]) == 3)
solver.push()
solver.add(opt_e_constr)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")