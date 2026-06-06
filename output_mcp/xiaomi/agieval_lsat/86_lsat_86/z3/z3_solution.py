from z3 import *

solver = Solver()

# Sales representatives
reps = ['Kim', 'Mahr', 'Parra', 'Quinn', 'Stuckey', 'Tiao', 'Udall']

# Zone assignments: each rep is assigned to zone 1, 2, or 3
zone = {r: Int(f'zone_{r}') for r in reps}

# Each rep works in exactly one zone (1, 2, or 3)
for r in reps:
    solver.add(Or(zone[r] == 1, zone[r] == 2, zone[r] == 3))

# Condition 1: Either Parra or Tiao (but not both) works in Zone 1
solver.add(Or(
    And(zone['Parra'] == 1, zone['Tiao'] != 1),
    And(zone['Parra'] != 1, zone['Tiao'] == 1)
))

# Condition 2: Either Tiao or Udall (but not both) works in Zone 2
solver.add(Or(
    And(zone['Tiao'] == 2, zone['Udall'] != 2),
    And(zone['Tiao'] != 2, zone['Udall'] == 2)
))

# Condition 3: Parra and Quinn work in the same zone
solver.add(zone['Parra'] == zone['Quinn'])

# Condition 4: Stuckey and Udall work in the same zone
solver.add(zone['Stuckey'] == zone['Udall'])

# Condition 5: More reps in Zone 3 than in Zone 2
count_z2 = Sum([If(zone[r] == 2, 1, 0) for r in reps])
count_z3 = Sum([If(zone[r] == 3, 1, 0) for r in reps])
solver.add(count_z3 > count_z2)

# Now test each option: "Quinn CANNOT work in the same zone as X"
# This means: for each option, check if it's possible for Quinn and X to be in the same zone.
# If it's NOT possible (unsat), then Quinn CANNOT work with X.
# We want the one where Quinn CANNOT work with them.

found_options = []
for letter, name in [("A", "Kim"), ("B", "Mahr"), ("C", "Stuckey"), ("D", "Tiao"), ("E", "Udall")]:
    solver.push()
    # Add constraint that Quinn and this person are in the same zone
    solver.add(zone['Quinn'] == zone[name])
    if solver.check() == sat:
        # It IS possible for Quinn to work with this person, so Quinn CAN work with them
        pass
    else:
        # It is NOT possible, so Quinn CANNOT work with this person
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