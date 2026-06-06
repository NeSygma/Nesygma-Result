from z3 import *

# Define variables for each representative's zone (1,2,3)
people = ['Kim','Mahr','Parra','Quinn','Stuckey','Tiao','Udall']
zone = {p: Int(p) for p in people}
solver = Solver()
# each zone in 1..3
for p in people:
    solver.add(And(zone[p] >= 1, zone[p] <= 3))
# Constraint 1: exactly one of Parra or Tiao in Zone1
solver.add(Or(And(zone['Parra'] == 1, zone['Tiao'] != 1),
               And(zone['Tiao'] == 1, zone['Parra'] != 1)))
# Constraint 2: exactly one of Tiao or Udall in Zone2
solver.add(Or(And(zone['Tiao'] == 2, zone['Udall'] != 2),
               And(zone['Udall'] == 2, zone['Tiao'] != 2)))
# Constraint 3: Parra and Quinn same zone
solver.add(zone['Parra'] == zone['Quinn'])
# Constraint 4: Stuckey and Udall same zone
solver.add(zone['Stuckey'] == zone['Udall'])
# Constraint 5: more in Zone3 than Zone2
cnt2 = Sum([If(zone[p] == 2, 1, 0) for p in people])
cnt3 = Sum([If(zone[p] == 3, 1, 0) for p in people])
solver.add(cnt3 > cnt2)

# Define option constraints
opt_a = And(
    zone['Kim'] == 1,
    zone['Parra'] == 1,
    zone['Stuckey'] == 2,
    zone['Udall'] == 2,
    zone['Mahr'] == 3,
    zone['Quinn'] == 3,
    zone['Tiao'] == 3
)
opt_b = And(
    zone['Kim'] == 1,
    zone['Tiao'] == 1,
    zone['Stuckey'] == 2,
    zone['Udall'] == 2,
    zone['Mahr'] == 3,
    zone['Parra'] == 3,
    zone['Quinn'] == 3
)
opt_c = And(
    zone['Parra'] == 1,
    zone['Quinn'] == 1,
    zone['Kim'] == 2,
    zone['Udall'] == 2,
    zone['Mahr'] == 3,
    zone['Stuckey'] == 3,
    zone['Tiao'] == 3
)
opt_d = And(
    zone['Stuckey'] == 1,
    zone['Udall'] == 1,
    zone['Kim'] == 2,
    zone['Tiao'] == 2,
    zone['Mahr'] == 3,
    zone['Parra'] == 3,
    zone['Quinn'] == 3
)
opt_e = And(
    zone['Tiao'] == 1,
    zone['Kim'] == 2,
    zone['Parra'] == 2,
    zone['Quinn'] == 2,
    zone['Stuckey'] == 3,
    zone['Udall'] == 3,
    zone['Mahr'] == 3  # Mahr not mentioned, assume Zone3 to fill remaining
)

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