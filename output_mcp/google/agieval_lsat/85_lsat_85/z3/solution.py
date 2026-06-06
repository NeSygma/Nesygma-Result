from z3 import *

# Reps
reps = ['Kim', 'Mahr', 'Parra', 'Quinn', 'Stuckey', 'Tiao', 'Udall']
# Zones 1, 2, 3
# Variables
zone = {r: Int(f'zone_{r}') for r in reps}

solver = Solver()

# Each rep in exactly one zone
for r in reps:
    solver.add(zone[r] >= 1, zone[r] <= 3)

# 1. Either Parra or Tiao (but not both) works in Zone 1.
solver.add(Xor(zone['Parra'] == 1, zone['Tiao'] == 1))

# 2. Either Tiao or Udall (but not both) works in Zone 2.
solver.add(Xor(zone['Tiao'] == 2, zone['Udall'] == 2))

# 3. Parra and Quinn work in the same sales zone as each other.
solver.add(zone['Parra'] == zone['Quinn'])

# 4. Stuckey and Udall work in the same sales zone as each other.
solver.add(zone['Stuckey'] == zone['Udall'])

# 5. There are more of the sales representatives working in Zone 3 than in Zone 2.
count2 = Sum([If(zone[r] == 2, 1, 0) for r in reps])
count3 = Sum([If(zone[r] == 3, 1, 0) for r in reps])
solver.add(count3 > count2)

# Options
options = {
    "A": ['Kim', 'Mahr'],
    "B": ['Kim', 'Tiao'],
    "C": ['Parra', 'Quinn'],
    "D": ['Stuckey', 'Tiao', 'Udall'],
    "E": ['Parra', 'Quinn', 'Stuckey', 'Udall']
}

found_options = []
for letter, zone3_reps in options.items():
    solver.push()
    # Add constraints for this option
    for r in reps:
        if r in zone3_reps:
            solver.add(zone[r] == 3)
        else:
            solver.add(zone[r] != 3)
    
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