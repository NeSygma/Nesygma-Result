from z3 import *
solver = Solver()
# declare days
H, L, M, S, T, V = Ints('H L M S T V')
# domain
for d in [H, L, M, S, T, V]:
    solver.add(d >= 1, d <= 6)
# distinct
solver.add(Distinct(H, L, M, S, T, V))
# constraints
solver.add(S != 1)
solver.add(Implies(H < L, M < L))
solver.add(S < M)
solver.add(S < V)
solver.add(Or(And(T < H, Not(T < V)), And(Not(T < H), T < V)))
# option constraints
opt_a_constr = (H == V - 1)
opt_b_constr = (L == V - 1)
opt_c_constr = (M == V - 1)
opt_d_constr = (S == V - 1)
opt_e_constr = (T == V - 1)
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