from z3 import *

# Variables for each representative's zone (1,2,3)
Kim = Int('Kim')
Mahr = Int('Mahr')
Parra = Int('Parra')
Quinn = Int('Quinn')
Stuckey = Int('Stuckey')
Tiao = Int('Tiao')
Udall = Int('Udall')
persons = [Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall]

solver = Solver()
# Domain constraints
for p in persons:
    solver.add(p >= 1, p <= 3)
# Base constraints
solver.add((If(Parra == 1, 1, 0) + If(Tiao == 1, 1, 0)) == 1)  # exactly one of Parra,Tiao in Zone1
solver.add((If(Tiao == 2, 1, 0) + If(Udall == 2, 1, 0)) == 1)  # exactly one of Tiao,Udall in Zone2
solver.add(Parra == Quinn)  # same zone
solver.add(Stuckey == Udall)  # same zone
# More in Zone3 than Zone2
count2 = Sum([If(p == 2, 1, 0) for p in persons])
count3 = Sum([If(p == 3, 1, 0) for p in persons])
solver.add(count3 > count2)

# Option constraints (the statement to test)
opt_a = And(Kim == 1, Stuckey == 1)
opt_b = And(Kim == 3, Stuckey == 3)
opt_c = And(Mahr == 3, Stuckey == 3)
opt_d = And(Mahr == 3, Udall == 3)
opt_e = And(Parra == 1, Stuckey == 1)

unsat_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
        unsat_options.append(letter)
    solver.pop()

if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
elif len(unsat_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options {unsat_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible option found")