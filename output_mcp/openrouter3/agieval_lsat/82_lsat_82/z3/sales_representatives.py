from z3 import *

# Define the sales representatives and zones
reps = ["Kim", "Mahr", "Parra", "Quinn", "Stuckey", "Tiao", "Udall"]
zones = [1, 2, 3]

# Create a mapping from each representative to their zone
# We'll use an integer variable for each representative (1, 2, or 3)
rep_zone = {rep: Int(f"zone_{rep}") for rep in reps}

solver = Solver()

# Add domain constraints: each representative works in exactly one zone (1, 2, or 3)
for rep in reps:
    solver.add(Or([rep_zone[rep] == z for z in zones]))

# Condition 1: Either Parra or Tiao (but not both) works in Zone 1
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
# Count representatives in each zone
count_zone_2 = Sum([If(rep_zone[rep] == 2, 1, 0) for rep in reps])
count_zone_3 = Sum([If(rep_zone[rep] == 3, 1, 0) for rep in reps])
solver.add(count_zone_3 > count_zone_2)

# Now evaluate each answer choice
found_options = []

# Option A: Zone 1: Kim, Parra; Zone 2: Stuckey, Udall; Zone 3: Mahr, Quinn, Tiao
opt_a = And(
    rep_zone["Kim"] == 1,
    rep_zone["Parra"] == 1,
    rep_zone["Stuckey"] == 2,
    rep_zone["Udall"] == 2,
    rep_zone["Mahr"] == 3,
    rep_zone["Quinn"] == 3,
    rep_zone["Tiao"] == 3
)

# Option B: Zone 1: Kim, Tiao; Zone 2: Stuckey, Udall; Zone 3: Mahr, Parra, Quinn
opt_b = And(
    rep_zone["Kim"] == 1,
    rep_zone["Tiao"] == 1,
    rep_zone["Stuckey"] == 2,
    rep_zone["Udall"] == 2,
    rep_zone["Mahr"] == 3,
    rep_zone["Parra"] == 3,
    rep_zone["Quinn"] == 3
)

# Option C: Zone 1: Parra, Quinn; Zone 2: Kim, Udall; Zone 3: Mahr, Stuckey, Tiao
opt_c = And(
    rep_zone["Parra"] == 1,
    rep_zone["Quinn"] == 1,
    rep_zone["Kim"] == 2,
    rep_zone["Udall"] == 2,
    rep_zone["Mahr"] == 3,
    rep_zone["Stuckey"] == 3,
    rep_zone["Tiao"] == 3
)

# Option D: Zone 1: Stuckey, Udall; Zone 2: Kim, Tiao; Zone 3: Mahr, Parra, Quinn
opt_d = And(
    rep_zone["Stuckey"] == 1,
    rep_zone["Udall"] == 1,
    rep_zone["Kim"] == 2,
    rep_zone["Tiao"] == 2,
    rep_zone["Mahr"] == 3,
    rep_zone["Parra"] == 3,
    rep_zone["Quinn"] == 3
)

# Option E: Zone 1: Tiao; Zone 2: Kim, Parra, Quinn; Zone 3: Stuckey, Udall
opt_e = And(
    rep_zone["Tiao"] == 1,
    rep_zone["Kim"] == 2,
    rep_zone["Parra"] == 2,
    rep_zone["Quinn"] == 2,
    rep_zone["Stuckey"] == 3,
    rep_zone["Udall"] == 3
)

# Test each option
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
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