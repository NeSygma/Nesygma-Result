from z3 import *

solver = Solver()

K, M, P, Q, S, T, U = Ints('K M P Q S T U')
reps = [K, M, P, Q, S, T, U]
for r in reps:
    solver.add(r >= 1, r <= 3)

solver.add(Or(P == 1, T == 1))
solver.add(Not(And(P == 1, T == 1)))

solver.add(Or(T == 2, U == 2))
solver.add(Not(And(T == 2, U == 2)))

solver.add(P == Q)
solver.add(S == U)

zone3_count = Sum([If(r == 3, 1, 0) for r in reps])
zone2_count = Sum([If(r == 2, 1, 0) for r in reps])
solver.add(zone3_count > zone2_count)

opt_a = And(K == 1, S == 1)
opt_b = And(K == 3, S == 3)
opt_c = And(M == 3, S == 3)
opt_d = And(M == 3, U == 3)
opt_e = And(P == 1, S == 1)

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