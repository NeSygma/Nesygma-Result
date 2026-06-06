from z3 import *

# Declare variables for each representative
Kim = Int('Kim')
Mahr = Int('Mahr')
Parra = Int('Parra')
Quinn = Int('Quinn')
Stuckey = Int('Stuckey')
Tiao = Int('Tiao')
Udall = Int('Udall')

persons = [Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall]

solver = Solver()

# Domain constraints: each in {1,2,3}
for p in persons:
    solver.add(p >= 1, p <= 3)

# Base constraints
# Either Parra or Tiao (but not both) works in Zone 1
solver.add((If(Parra == 1, 1, 0) + If(Tiao == 1, 1, 0)) == 1)
# Either Tiao or Udall (but not both) works in Zone 2
solver.add((If(Tiao == 2, 1, 0) + If(Udall == 2, 1, 0)) == 1)
# Parra and Quinn same zone
solver.add(Parra == Quinn)
# Stuckey and Udall same zone
solver.add(Stuckey == Udall)
# More reps in Zone 3 than in Zone 2
count2 = Sum([If(p == 2, 1, 0) for p in persons])
count3 = Sum([If(p == 3, 1, 0) for p in persons])
solver.add(count3 > count2)

# Option constraints
opt_a_constr = And(Kim == 1, Stuckey == 1)
opt_b_constr = And(Kim == 3, Stuckey == 3)
opt_c_constr = And(Mahr == 3, Stuckey == 3)
opt_d_constr = And(Mahr == 3, Udall == 3)
opt_e_constr = And(Parra == 1, Stuckey == 1)

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