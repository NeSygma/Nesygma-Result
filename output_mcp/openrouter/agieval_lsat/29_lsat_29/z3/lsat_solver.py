from z3 import *

# Declare boolean variables for each scientist
F, G, H = Bools('F G H')
K, L, M = Bools('K L M')
P, Q, R = Bools('P Q R')

solver = Solver()

# Exactly 5 selected
selected = [F, G, H, K, L, M, P, Q, R]
solver.add(Sum([If(v, 1, 0) for v in selected]) == 5)

# At least one of each type
solver.add(Sum([If(v, 1, 0) for v in [F, G, H]]) >= 1)
solver.add(Sum([If(v, 1, 0) for v in [K, L, M]]) >= 1)
solver.add(Sum([If(v, 1, 0) for v in [P, Q, R]]) >= 1)

# If more than one botanist, then at most one zoologist
bot_sum = Sum([If(v, 1, 0) for v in [F, G, H]])
zoo_sum = Sum([If(v, 1, 0) for v in [P, Q, R]])
solver.add(Or(bot_sum <= 1, zoo_sum <= 1))

# F and K cannot both be selected
solver.add(Or(Not(F), Not(K)))
# K and M cannot both be selected
solver.add(Or(Not(K), Not(M)))
# If M selected, both P and R must be selected
solver.add(Or(Not(M), And(P, R)))

# Premise: both G and H are selected
solver.add(G == True, H == True)

# Define option constraints
opt_a = Or(F, K)   # A: F or K
opt_b = Or(F, M)   # B: F or M
opt_c = Or(K, M)   # C: K or M
opt_d = Or(M, Q)   # D: M or Q
opt_e = Or(P, Q)   # E: P or Q

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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