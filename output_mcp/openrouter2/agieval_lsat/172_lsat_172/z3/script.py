from z3 import *
solver = Solver()
# declare variables
L_F, L_G, L_H = Ints('L_F L_G L_H')
M_F, M_G, M_H = Ints('M_F M_G M_H')
S_F, S_G, S_H = Ints('S_F S_G S_H')

# non-negativity
solver.add(L_F >= 0, L_G >= 0, L_H >= 0)
solver.add(M_F >= 0, M_G >= 0, M_H >= 0)
solver.add(S_F >= 0, S_G >= 0, S_H >= 0)

# section sums
solver.add(L_F + L_G + L_H == 2)
solver.add(M_F + M_G + M_H == 2)
solver.add(S_F + S_G + S_H == 2)

# given L_F=1, L_H=1, L_G=0
solver.add(L_F == 1, L_H == 1, L_G == 0)

# given S_F=1, S_G=0
solver.add(S_F == 1, S_G == 0)

# G cannot be in Sports
solver.add(S_G == 0)

# Hue's photos in L equals Fuentes in S
solver.add(L_H == S_F)

# at least one photographer in L also in M
solver.add(Or(M_F > 0, M_H > 0))

# total per photographer between 1 and 3
solver.add(L_F + M_F + S_F >= 1, L_F + M_F + S_F <= 3)
solver.add(L_G + M_G + S_G >= 1, L_G + M_G + S_G <= 3)
solver.add(L_H + M_H + S_H >= 1, L_H + M_H + S_H <= 3)

# define option constraints
opt_a_constr = M_F == 2
opt_b_constr = M_G == 2
opt_c_constr = M_H == 1
opt_d_constr = S_H == 2
opt_e_constr = S_H == 0

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