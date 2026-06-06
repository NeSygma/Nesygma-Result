from z3 import *

# Sales representatives
reps = ['Kim', 'Mahr', 'Parra', 'Quinn', 'Stuckey', 'Tiao', 'Udall']

# Zone assignment: each rep gets a zone (1, 2, or 3)
zone = {r: Int(f'zone_{r}') for r in reps}

solver = Solver()

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
# Count reps in each zone
count_z2 = Sum([If(zone[r] == 2, 1, 0) for r in reps])
count_z3 = Sum([If(zone[r] == 3, 1, 0) for r in reps])
solver.add(count_z3 > count_z2)

# Now define each option as constraints
# Option A: Zone 1: Kim, Parra; Zone 2: Stuckey, Udall; Zone 3: Mahr, Quinn, Tiao
opt_a_constr = And(
    zone['Kim'] == 1, zone['Parra'] == 1,
    zone['Stuckey'] == 2, zone['Udall'] == 2,
    zone['Mahr'] == 3, zone['Quinn'] == 3, zone['Tiao'] == 3
)

# Option B: Zone 1: Kim, Tiao; Zone 2: Stuckey, Udall; Zone 3: Mahr, Parra, Quinn
opt_b_constr = And(
    zone['Kim'] == 1, zone['Tiao'] == 1,
    zone['Stuckey'] == 2, zone['Udall'] == 2,
    zone['Mahr'] == 3, zone['Parra'] == 3, zone['Quinn'] == 3
)

# Option C: Zone 1: Parra, Quinn; Zone 2: Kim, Udall; Zone 3: Mahr, Stuckey, Tiao
opt_c_constr = And(
    zone['Parra'] == 1, zone['Quinn'] == 1,
    zone['Kim'] == 2, zone['Udall'] == 2,
    zone['Mahr'] == 3, zone['Stuckey'] == 3, zone['Tiao'] == 3
)

# Option D: Zone 1: Stuckey, Udall; Zone 2: Kim, Tiao; Zone 3: Mahr, Parra, Quinn
opt_d_constr = And(
    zone['Stuckey'] == 1, zone['Udall'] == 1,
    zone['Kim'] == 2, zone['Tiao'] == 2,
    zone['Mahr'] == 3, zone['Parra'] == 3, zone['Quinn'] == 3
)

# Option E: Zone 1: Tiao; Zone 2: Kim, Parra, Quinn; Zone 3: Stuckey, Udall
opt_e_constr = And(
    zone['Tiao'] == 1,
    zone['Kim'] == 2, zone['Parra'] == 2, zone['Quinn'] == 2,
    zone['Stuckey'] == 3, zone['Udall'] == 3
)

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