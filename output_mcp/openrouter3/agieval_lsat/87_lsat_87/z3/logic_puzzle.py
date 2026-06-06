from z3 import *

# Create solver
solver = Solver()

# Define representatives and zones
reps = ["Kim", "Mahr", "Parra", "Quinn", "Stuckey", "Tiao", "Udall"]
zones = [1, 2, 3]

# Create assignment variables: rep_zone[rep] = zone number
rep_zone = {rep: Int(f"zone_{rep}") for rep in reps}

# Domain constraints: each rep works in exactly one zone (1, 2, or 3)
for rep in reps:
    solver.add(Or([rep_zone[rep] == z for z in zones]))

# Condition 1: Either Parra or Tiao (but not both) works in Zone 1
# This means exactly one of them is in zone 1
solver.add(Or(rep_zone["Parra"] == 1, rep_zone["Tiao"] == 1))
solver.add(Not(And(rep_zone["Parra"] == 1, rep_zone["Tiao"] == 1)))

# Condition 2: Either Tiao or Udall (but not both) works in Zone 2
solver.add(Or(rep_zone["Tiao"] == 2, rep_zone["Udall"] == 2))
solver.add(Not(And(rep_zone["Tiao"] == 2, rep_zone["Udall"] == 2)))

# Condition 3: Parra and Quinn work in the same sales zone as each other
solver.add(rep_zone["Parra"] == rep_zone["Quinn"])

# Condition 4: Stuckey and Udall work in the same sales zone as each other
solver.add(rep_zone["Stuckey"] == rep_zone["Udall"])

# Condition 5: There are more of the sales representatives working in Zone 3 than in Zone 2
# Count reps in each zone
count_zone2 = Sum([If(rep_zone[rep] == 2, 1, 0) for rep in reps])
count_zone3 = Sum([If(rep_zone[rep] == 3, 1, 0) for rep in reps])
solver.add(count_zone3 > count_zone2)

# Additional constraint: Mahr and Stuckey work in the same sales zone
# This is the premise for the question
solver.add(rep_zone["Mahr"] == rep_zone["Stuckey"])

# Now evaluate each answer choice
found_options = []

# Option A: Kim works in Zone 2
opt_a = (rep_zone["Kim"] == 2)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Mahr works in Zone 1
opt_b = (rep_zone["Mahr"] == 1)
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Parra works in Zone 3
opt_c = (rep_zone["Parra"] == 3)
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Stuckey works in Zone 2
opt_d = (rep_zone["Stuckey"] == 2)
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Tiao works in Zone 1
opt_e = (rep_zone["Tiao"] == 1)
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Print results according to the required format
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")