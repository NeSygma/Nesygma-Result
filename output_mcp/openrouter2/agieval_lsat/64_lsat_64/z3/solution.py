from z3 import *

solver = Solver()

# Variables: bicycle indices 0=F,1=G,2=H,3=J
R1, S1, T1, Y1 = Ints('R1 S1 T1 Y1')
R2, S2, T2, Y2 = Ints('R2 S2 T2 Y2')

# Domain constraints
for v in [R1, S1, T1, Y1, R2, S2, T2, Y2]:
    solver.add(v >= 0, v <= 3)

# Distinct bicycles each day
solver.add(Distinct(R1, S1, T1, Y1))
solver.add(Distinct(R2, S2, T2, Y2))

# Constraints from the problem
solver.add(R1 != 0, R2 != 0)          # Reynaldo cannot test F
solver.add(Y1 != 3, Y2 != 3)          # Yuki cannot test J
solver.add(Or(T1 == 2, T2 == 2))      # Theresa must test H on one day
solver.add(Y1 == S2)                  # Yuki's first day bike is Seamus's second day bike

# Assumption for the question
solver.add(T1 == 3)                   # Theresa tests J on the first day

# Option constraints
opt_a_constr = R2 == 1                # Reynaldo tests G on the second day
opt_b_constr = S1 == 2                # Seamus tests H on the first day
opt_c_constr = Y2 == 2                # Yuki tests H on the second day
opt_d_constr = Or(S1 == 3, S2 == 3)   # Seamus tests J on either day
opt_e_constr = Or(T1 == 1, T2 == 1)   # Theresa tests G on either day

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr),
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
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