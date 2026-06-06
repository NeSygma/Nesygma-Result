from z3 import *

solver = Solver()
# Define variables for each sales representative
Kim = Int('Kim')
Mahr = Int('Mahr')
Parra = Int('Parra')
Quinn = Int('Quinn')
Stuckey = Int('Stuckey')
Tiao = Int('Tiao')
Udall = Int('Udall')

# Domain constraints: each rep works in exactly one of the three zones (1,2,3)
for rep in [Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall]:
    solver.add(rep >= 1, rep <= 3)

# Either Parra or Tiao (but not both) works in Zone 1
solver.add(Xor(Parra == 1, Tiao == 1))
# Either Tiao or Udall (but not both) works in Zone 2
solver.add(Xor(Tiao == 2, Udall == 2))
# Parra and Quinn work in the same zone
solver.add(Parra == Quinn)
# Stuckey and Udall work in the same zone
solver.add(Stuckey == Udall)

# Count of reps in each zone
reps = [Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall]
count1 = Sum([If(rep == 1, 1, 0) for rep in reps])
count2 = Sum([If(rep == 2, 1, 0) for rep in reps])
count3 = Sum([If(rep == 3, 1, 0) for rep in reps])

# There are more reps in Zone 3 than in Zone 2
solver.add(count3 > count2)
# If more reps work in Zone 1 than in Zone 3
solver.add(count1 > count3)

# Define option constraints
opt_a_constr = Kim == 2
opt_b_constr = Mahr == 2
opt_c_constr = Parra == 3
opt_d_constr = Tiao == 1
opt_e_constr = Udall == 3

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