from z3 import *
solver = Solver()
# define singers and positions
singers = ['Kammer', 'Lugo', 'Trillo', 'Waite', 'Yoshida', 'Zinn']
pos = {s: Int(s) for s in singers}

# base constraints
base_constraints = []
for s in singers:
    base_constraints.append(pos[s] >= 1)
    base_constraints.append(pos[s] <= 6)
base_constraints.append(Distinct([pos[s] for s in singers]))
base_constraints.append(pos['Kammer'] != 4)
base_constraints.append(pos['Lugo'] != 4)
base_constraints.append(Or(pos['Kammer'] == 5, pos['Lugo'] == 5))
base_constraints.append(pos['Waite'] < pos['Kammer'])
base_constraints.append(pos['Waite'] < pos['Lugo'])
base_constraints.append(pos['Kammer'] < pos['Trillo'])
base_constraints.append(pos['Zinn'] < pos['Yoshida'])

# ordering constraints for each option
opt_a_order = [pos['Kammer']==1, pos['Trillo']==2, pos['Zinn']==3, pos['Waite']==4, pos['Lugo']==5, pos['Yoshida']==6]
opt_b_order = [pos['Waite']==1, pos['Kammer']==2, pos['Yoshida']==3, pos['Zinn']==4, pos['Lugo']==5, pos['Trillo']==6]
opt_c_order = [pos['Waite']==1, pos['Lugo']==2, pos['Kammer']==3, pos['Trillo']==4, pos['Zinn']==5, pos['Yoshida']==6]
opt_d_order = [pos['Waite']==1, pos['Zinn']==2, pos['Kammer']==3, pos['Trillo']==4, pos['Lugo']==5, pos['Yoshida']==6]
opt_e_order = [pos['Zinn']==1, pos['Yoshida']==2, pos['Waite']==3, pos['Lugo']==4, pos['Kammer']==5, pos['Trillo']==6]

opt_a_constr = And(base_constraints + opt_a_order)
opt_b_constr = And(base_constraints + opt_b_order)
opt_c_constr = And(base_constraints + opt_c_order)
opt_d_constr = And(base_constraints + opt_d_order)
opt_e_constr = And(base_constraints + opt_e_order)

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