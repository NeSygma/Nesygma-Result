from z3 import *

# Create solver
solver = Solver()

# Declare zone variables for each person (1, 2, or 3)
Kim = Int('Kim')
Mahr = Int('Mahr')
Parra = Int('Parra')
Quinn = Int('Quinn')
Stuckey = Int('Stuckey')
Tiao = Int('Tiao')
Udall = Int('Udall')

# All zones must be 1, 2, or 3
people = [Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall]
for p in people:
    solver.add(Or(p == 1, p == 2, p == 3))

# Constraint 1: Either Parra or Tiao (but not both) works in Zone 1
solver.add(Or(And(Parra == 1, Tiao != 1), And(Parra != 1, Tiao == 1)))

# Constraint 2: Either Tiao or Udall (but not both) works in Zone 2
solver.add(Or(And(Tiao == 2, Udall != 2), And(Tiao != 2, Udall == 2)))

# Constraint 3: Parra and Quinn work in the same zone
solver.add(Parra == Quinn)

# Constraint 4: Stuckey and Udall work in the same zone
solver.add(Stuckey == Udall)

# Constraint 5: More reps in Zone 3 than in Zone 2
zone3_count = Sum([If(p == 3, 1, 0) for p in people])
zone2_count = Sum([If(p == 2, 1, 0) for p in people])
solver.add(zone3_count > zone2_count)

# Now test each option: force Quinn to be in the same zone as each person
# We want to find which option makes the problem UNSATISFIABLE
opt_a_constr = (Quinn == Kim)
opt_b_constr = (Quinn == Mahr)
opt_c_constr = (Quinn == Stuckey)
opt_d_constr = (Quinn == Tiao)
opt_e_constr = (Quinn == Udall)

unsat_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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
    print(f"Refine: Multiple options found {unsat_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")