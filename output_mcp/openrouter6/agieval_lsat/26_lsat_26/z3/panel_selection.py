from z3 import *

solver = Solver()

# Declare selection variables
selected_F = Bool('selected_F')
selected_G = Bool('selected_G')
selected_H = Bool('selected_H')
selected_K = Bool('selected_K')
selected_L = Bool('selected_L')
selected_M = Bool('selected_M')
selected_P = Bool('selected_P')
selected_Q = Bool('selected_Q')
selected_R = Bool('selected_R')

# Helper counts
botanists = [selected_F, selected_G, selected_H]
chemists = [selected_K, selected_L, selected_M]
zoologists = [selected_P, selected_Q, selected_R]

botanist_count = Sum([If(b, 1, 0) for b in botanists])
chemist_count = Sum([If(c, 1, 0) for c in chemists])
zoologist_count = Sum([If(z, 1, 0) for z in zoologists])
total_selected = Sum([If(v, 1, 0) for v in [selected_F, selected_G, selected_H,
                                            selected_K, selected_L, selected_M,
                                            selected_P, selected_Q, selected_R]])

# Base constraints
solver.add(total_selected == 5)
solver.add(botanist_count >= 1)
solver.add(chemist_count >= 1)
solver.add(zoologist_count >= 1)

# If more than one botanist, then at most one zoologist
solver.add(Or(botanist_count <= 1, zoologist_count <= 1))

# F and K cannot both be selected
solver.add(Not(And(selected_F, selected_K)))

# K and M cannot both be selected
solver.add(Not(And(selected_K, selected_M)))

# If M selected, both P and R must be selected
solver.add(Implies(selected_M, And(selected_P, selected_R)))

# Extra condition: M is the only chemist selected
solver.add(selected_M == True)
solver.add(selected_K == False)
solver.add(selected_L == False)

# Define option constraints
opt_a = And(selected_F, selected_G)
opt_b = And(selected_G, selected_H)
opt_c = And(selected_H, selected_P)
opt_d = And(selected_F, selected_G, selected_H)
opt_e = And(selected_P, selected_Q, selected_R)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output result
BENCHMARK_MODE = True
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")