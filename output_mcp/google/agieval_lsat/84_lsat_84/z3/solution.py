from z3 import *

# Reps
reps = ['Kim', 'Mahr', 'Parra', 'Quinn', 'Stuckey', 'Tiao', 'Udall']
# Zones 1, 2, 3
# Map each rep to a zone variable
zone = {r: Int(r) for r in reps}

solver = Solver()

# Each rep works in exactly one zone
for r in reps:
    solver.add(zone[r] >= 1, zone[r] <= 3)

# Condition 1: Either Parra or Tiao (but not both) works in Zone 1.
solver.add(Xor(zone['Parra'] == 1, zone['Tiao'] == 1))

# Condition 2: Either Tiao or Udall (but not both) works in Zone 2.
solver.add(Xor(zone['Tiao'] == 2, zone['Udall'] == 2))

# Condition 3: Parra and Quinn work in the same sales zone as each other.
solver.add(zone['Parra'] == zone['Quinn'])

# Condition 4: Stuckey and Udall work in the same sales zone as each other.
solver.add(zone['Stuckey'] == zone['Udall'])

# Condition 5: There are more of the sales representatives working in Zone 3 than in Zone 2.
count_z3 = Sum([If(zone[r] == 3, 1, 0) for r in reps])
count_z2 = Sum([If(zone[r] == 2, 1, 0) for r in reps])
solver.add(count_z3 > count_z2)

# Options
options = {
    "A": And(zone['Kim'] == 1, zone['Stuckey'] == 1),
    "B": And(zone['Kim'] == 3, zone['Stuckey'] == 3),
    "C": And(zone['Mahr'] == 3, zone['Stuckey'] == 3),
    "D": And(zone['Mahr'] == 3, zone['Udall'] == 3),
    "E": And(zone['Parra'] == 1, zone['Stuckey'] == 1)
}

# We want to find which option MUST be false.
# An option must be false if it is impossible (unsat).
# So we check each option: if it is unsat, it must be false.

found_must_be_false = []
for letter, constr in options.items():
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
        found_must_be_false.append(letter)
    solver.pop()

if len(found_must_be_false) == 1:
    print("STATUS: sat")
    print(f"answer:{found_must_be_false[0]}")
elif len(found_must_be_false) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_must_be_false}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")