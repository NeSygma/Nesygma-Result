from z3 import *

# Declare variables for each antique
day_H = Int('day_H')  # harmonica
day_L = Int('day_L')  # lamp
day_M = Int('day_M')  # mirror
day_S = Int('day_S')  # sundial
day_T = Int('day_T')  # table
day_V = Int('day_V')  # vase

solver = Solver()

# Domain constraints: each day 1..6 and all distinct
vars = [day_H, day_L, day_M, day_S, day_T, day_V]
for v in vars:
    solver.add(v >= 1, v <= 6)
solver.add(Distinct(vars))

# Problem constraints
# 1. Sundial not on June 1st
solver.add(day_S != 1)
# 2. If harmonica earlier than lamp then mirror earlier than lamp
solver.add(Implies(day_H < day_L, day_M < day_L))
# 3. Sundial earlier than mirror and vase
solver.add(day_S < day_M)
solver.add(day_S < day_V)
# 4. Table earlier than harmonica XOR earlier than vase (exactly one)
solver.add(Xor(day_T < day_H, day_T < day_V))

# Option constraints (each option fixes the days according to the ordering)
opt_a_constr = And(day_H == 1, day_T == 2, day_S == 3, day_L == 4, day_V == 5, day_M == 6)
opt_b_constr = And(day_L == 1, day_H == 2, day_S == 3, day_M == 4, day_V == 5, day_T == 6)
opt_c_constr = And(day_H == 1, day_S == 2, day_T == 3, day_M == 4, day_L == 5, day_V == 6)
opt_d_constr = And(day_S == 1, day_M == 2, day_H == 3, day_T == 4, day_V == 5, day_L == 6)
opt_e_constr = And(day_V == 1, day_S == 2, day_L == 3, day_H == 4, day_T == 5, day_M == 6)

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