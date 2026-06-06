from z3 import *

solver = Solver()

# Reps and zone variables
reps = ['Kim','Mahr','Parra','Quinn','Stuckey','Tiao','Udall']
zone = {r: Int(f'zone_{r}') for r in reps}

# Domain constraints: zones 1-3
for r in reps:
    solver.add(zone[r] >= 1, zone[r] <= 3)

# Base constraints
# Either Parra or Tiao (but not both) works in Zone 1
solver.add(Xor(zone['Parra'] == 1, zone['Tiao'] == 1))
# Either Tiao or Udall (but not both) works in Zone 2
solver.add(Xor(zone['Tiao'] == 2, zone['Udall'] == 2))
# Parra and Quinn work in the same sales zone as each other
solver.add(zone['Parra'] == zone['Quinn'])
# Stuckey and Udall work in the same sales zone as each other
solver.add(zone['Stuckey'] == zone['Udall'])
# There are more of the sales representatives working in Zone 3 than in Zone 2
cnt3 = Sum([If(zone[r] == 3, 1, 0) for r in reps])
cnt2 = Sum([If(zone[r] == 2, 1, 0) for r in reps])
solver.add(cnt3 > cnt2)

# Option constraints
opt_a_constr = And([zone['Kim'] == 3, zone['Mahr'] == 3] + [zone[r] != 3 for r in reps if r not in ['Kim','Mahr']])
opt_b_constr = And([zone['Kim'] == 3, zone['Tiao'] == 3] + [zone[r] != 3 for r in reps if r not in ['Kim','Tiao']])
opt_c_constr = And([zone['Parra'] == 3, zone['Quinn'] == 3] + [zone[r] != 3 for r in reps if r not in ['Parra','Quinn']])
opt_d_constr = And([zone['Stuckey'] == 3, zone['Tiao'] == 3, zone['Udall'] == 3] + [zone[r] != 3 for r in reps if r not in ['Stuckey','Tiao','Udall']])
opt_e_constr = And([zone['Parra'] == 3, zone['Quinn'] == 3, zone['Stuckey'] == 3, zone['Udall'] == 3] + [zone[r] != 3 for r in reps if r not in ['Parra','Quinn','Stuckey','Udall']])

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