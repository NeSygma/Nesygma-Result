from z3 import *

solver = Solver()
# Variables: True = Fall, False = Spring
fall_K = Bool('fall_K')
fall_L = Bool('fall_L')
fall_M = Bool('fall_M')
fall_N = Bool('fall_N')
fall_O = Bool('fall_O')
fall_P = Bool('fall_P')

# Base constraints
# M and P cannot be in same season
solver.add(fall_M != fall_P)
# K and N same season
solver.add(fall_K == fall_N)
# If K fall then O fall
solver.add(Implies(fall_K, fall_O))
# If M fall then N spring
solver.add(Implies(fall_M, Not(fall_N)))
# Premise: N is fall
solver.add(fall_N == True)

# Option constraints
opt_a_constr = Not(fall_K)          # K is spring
opt_b_constr = fall_L == True        # L is fall
opt_c_constr = fall_M == True        # M is fall
opt_d_constr = Not(fall_O)          # O is spring
opt_e_constr = Not(fall_P)          # P is spring

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