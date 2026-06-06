from z3 import *
solver = Solver()

# Define position variables
pos_K = Int('pos_K')
pos_L = Int('pos_L')
pos_T = Int('pos_T')
pos_W = Int('pos_W')
pos_Y = Int('pos_Y')
pos_Z = Int('pos_Z')

# Base constraints
solver.add(pos_K >= 1, pos_K <= 6)
solver.add(pos_L >= 1, pos_L <= 6)
solver.add(pos_T >= 1, pos_T <= 6)
solver.add(pos_W >= 1, pos_W <= 6)
solver.add(pos_Y >= 1, pos_Y <= 6)
solver.add(pos_Z >= 1, pos_Z <= 6)

solver.add(Distinct([pos_K, pos_L, pos_T, pos_W, pos_Y, pos_Z]))

# Constraints
solver.add(pos_K != 4)
solver.add(pos_L != 4)
solver.add(Or(pos_K == 5, pos_L == 5))
solver.add(pos_W < pos_K)
solver.add(pos_W < pos_L)
solver.add(pos_K < pos_T)
solver.add(pos_Z < pos_Y)

# Define option constraints
opt_a_constr = (pos_K == 6)
opt_b_constr = (pos_L == 6)
opt_c_constr = (pos_T == 6)
opt_d_constr = (pos_W == 6)
opt_e_constr = (pos_Z == 6)

found_options = []
for letter, constr in [('A', opt_a_constr), ('B', opt_b_constr), ('C', opt_c_constr), ('D', opt_d_constr), ('E', opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print('STATUS: sat')
    print(f'answer:{found_options[0]}')
elif len(found_options) > 1:
    print('STATUS: unsat')
    print(f'Refine: Multiple options found {found_options}')
else:
    print('STATUS: unsat')
    print('Refine: No options found')