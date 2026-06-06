from z3 import *

solver = Solver()

selected_F, selected_G, selected_H = Bools('F G H')
selected_K, selected_L, selected_M = Bools('K L M')
selected_P, selected_Q, selected_R = Bools('P Q R')

# Exactly 5 selected
solver.add(Sum([If(selected_F,1,0), If(selected_G,1,0), If(selected_H,1,0),
                If(selected_K,1,0), If(selected_L,1,0), If(selected_M,1,0),
                If(selected_P,1,0), If(selected_Q,1,0), If(selected_R,1,0)]) == 5)

# At least one of each type
solver.add(Or(selected_F, selected_G, selected_H))
solver.add(Or(selected_K, selected_L, selected_M))
solver.add(Or(selected_P, selected_Q, selected_R))

# If more than one botanist, then at most one zoologist
botanists = Sum([If(selected_F,1,0), If(selected_G,1,0), If(selected_H,1,0)])
zoologists = Sum([If(selected_P,1,0), If(selected_Q,1,0), If(selected_R,1,0)])
solver.add(Implies(botanists > 1, zoologists <= 1))

# F and K cannot both
solver.add(Not(And(selected_F, selected_K)))

# K and M cannot both
solver.add(Not(And(selected_K, selected_M)))

# If M then both P and R
solver.add(Implies(selected_M, And(selected_P, selected_R)))

# Given: P is the only zoologist selected
solver.add(selected_P)
solver.add(Not(selected_Q))
solver.add(Not(selected_R))

# Helper for chemists count
chemists = Sum([If(selected_K,1,0), If(selected_L,1,0), If(selected_M,1,0)])

# Evaluate each option

# Option A: If K selected, G cannot be selected. Negation: K and G
solver.push()
solver.add(And(selected_K, selected_G))
result_a = solver.check()
solver.pop()

# Option B: If L selected, F cannot be selected. Negation: L and F
solver.push()
solver.add(And(selected_L, selected_F))
result_b = solver.check()
solver.pop()

# Option C: If exactly one chemist selected, it must be K. Negation: exactly 1 chemist and not K
solver.push()
solver.add(chemists == 1)
solver.add(Not(selected_K))
result_c = solver.check()
solver.pop()

# Option D: If exactly two chemists selected, F cannot be selected. Negation: 2 chemists and F
solver.push()
solver.add(chemists == 2)
solver.add(selected_F)
result_d = solver.check()
solver.pop()

# Option E: If exactly two chemists selected, G cannot be selected. Negation: 2 chemists and G
solver.push()
solver.add(chemists == 2)
solver.add(selected_G)
result_e = solver.check()
solver.pop()

found_options = []
if result_a == unsat:
    found_options.append('A')
if result_b == unsat:
    found_options.append('B')
if result_c == unsat:
    found_options.append('C')
if result_d == unsat:
    found_options.append('D')
if result_e == unsat:
    found_options.append('E')

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")