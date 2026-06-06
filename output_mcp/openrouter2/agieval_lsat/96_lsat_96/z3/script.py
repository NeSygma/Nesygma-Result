from z3 import *
solver = Solver()
# positions
pos_J = Int('pos_J')
pos_K = Int('pos_K')
pos_L = Int('pos_L')
pos_M = Int('pos_M')
pos_N = Int('pos_N')
pos_O = Int('pos_O')
pos_P = Int('pos_P')
# domain
solver.add(pos_J >= 1, pos_J <= 7)
solver.add(pos_K >= 1, pos_K <= 7)
solver.add(pos_L >= 1, pos_L <= 7)
solver.add(pos_M >= 1, pos_M <= 7)
solver.add(pos_N >= 1, pos_N <= 7)
solver.add(pos_O >= 1, pos_O <= 7)
solver.add(pos_P >= 1, pos_P <= 7)
# distinct
solver.add(Distinct(pos_J, pos_K, pos_L, pos_M, pos_N, pos_O, pos_P))
# J in evening
solver.add(Or(pos_J == 6, pos_J == 7))
# K not in morning
solver.add(And(pos_K != 1, pos_K != 2))
# L after K
solver.add(pos_L > pos_K)
# L before M
solver.add(pos_L < pos_M)
# options
opt_a_constr = pos_K > pos_J
opt_b_constr = pos_L > pos_J
opt_c_constr = pos_P > pos_J
opt_d_constr = And(pos_N > pos_M, pos_O > pos_M)
opt_e_constr = And(pos_N > pos_K, pos_P > pos_K)
# evaluate
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