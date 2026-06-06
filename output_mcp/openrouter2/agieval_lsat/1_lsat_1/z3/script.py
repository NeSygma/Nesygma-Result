from z3 import *

solver = Solver()
# Define slot variables: 0=Mon morning, 1=Mon afternoon, 2=Tue morning, 3=Tue afternoon, 4=Wed morning, 5=Wed afternoon
s0, s1, s2, s3, s4, s5 = Ints('s0 s1 s2 s3 s4 s5')
# Domain constraints: each slot assigned a student index 0..7
for s in [s0, s1, s2, s3, s4, s5]:
    solver.add(s >= 0, s <= 7)
# All slots must have distinct students
solver.add(Distinct(s0, s1, s2, s3, s4, s5))
# Tuesday is the only day George (0) can give a report
solver.add(Not(s0 == 0), Not(s1 == 0), Not(s4 == 0), Not(s5 == 0))
solver.add(Or(s2 == 0, s3 == 0))
# Olivia (6) and Robert (7) cannot give an afternoon report
solver.add(Not(s1 == 6), Not(s3 == 6), Not(s5 == 6))
solver.add(Not(s1 == 7), Not(s3 == 7), Not(s5 == 7))
# Nina rule
n_monday = Or(s0 == 5, s1 == 5)
n_tuesday = Or(s2 == 5, s3 == 5)
# n_wednesday = Or(s4 == 5, s5 == 5)  # no requirement if on Wed
solver.add(Implies(n_monday, And(Or(s2 == 1, s3 == 1), Or(s2 == 2, s3 == 2))))
solver.add(Implies(n_tuesday, And(Or(s4 == 1, s5 == 1), Or(s4 == 2, s5 == 2))))

# Define option constraints
opt_a_constr = And(s0 == 1, s1 == 7, s2 == 6, s3 == 2, s4 == 4, s5 == 3)
opt_b_constr = And(s0 == 2, s1 == 6, s2 == 1, s3 == 3, s4 == 5, s5 == 4)
opt_c_constr = And(s0 == 4, s1 == 1, s2 == 0, s3 == 3, s4 == 7, s5 == 2)
opt_d_constr = And(s0 == 5, s1 == 1, s2 == 7, s3 == 2, s4 == 6, s5 == 4)
opt_e_constr = And(s0 == 6, s1 == 5, s2 == 2, s3 == 1, s4 == 3, s5 == 0)

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