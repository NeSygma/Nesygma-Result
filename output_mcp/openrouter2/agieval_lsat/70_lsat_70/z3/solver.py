from z3 import *

# Define solver
solver = Solver()

# Books as Int variables representing shelf index: 0=top,1=middle,2=bottom
F, G, H, I, K, L, M, O = Ints('F G H I K L M O')
books = [F, G, H, I, K, L, M, O]

# Domain constraints
for b in books:
    solver.add(And(b >= 0, b <= 2))

# Base constraints
# I on middle shelf
solver.add(I == 1)
# K higher than F (lower index)
solver.add(K < F)
# O higher than L
solver.add(O < L)
# F same shelf as M
solver.add(F == M)
# L higher than H (additional condition for question)
solver.add(L < H)

# At least two books per shelf
for s in range(3):
    count_s = Sum([If(b == s, 1, 0) for b in books])
    solver.add(count_s >= 2)

# More books on bottom than top
count_bottom = Sum([If(b == 2, 1, 0) for b in books])
count_top = Sum([If(b == 0, 1, 0) for b in books])
solver.add(count_bottom > count_top)

# Define option constraints
opt_a_constr = (F == G)
opt_b_constr = (G == H)
opt_c_constr = (H == M)
opt_d_constr = (I == G)
opt_e_constr = (K == O)

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