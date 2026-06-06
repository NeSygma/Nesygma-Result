from z3 import *

# Seven sales representatives
reps = ["Kim", "Mahr", "Parra", "Quinn", "Stuckey", "Tiao", "Udall"]

# Zones: 1, 2, 3
# We'll use integer variables for each rep's zone
zone = {r: Int(f"zone_{r}") for r in reps}

solver = Solver()

# Each rep works in exactly one of zones 1, 2, or 3
for r in reps:
    solver.add(Or(zone[r] == 1, zone[r] == 2, zone[r] == 3))

# Condition 1: Either Parra or Tiao (but not both) works in Zone 1.
solver.add(Or(
    And(zone["Parra"] == 1, zone["Tiao"] != 1),
    And(zone["Tiao"] == 1, zone["Parra"] != 1)
))

# Condition 2: Either Tiao or Udall (but not both) works in Zone 2.
solver.add(Or(
    And(zone["Tiao"] == 2, zone["Udall"] != 2),
    And(zone["Udall"] == 2, zone["Tiao"] != 2)
))

# Condition 3: Parra and Quinn work in the same sales zone as each other.
solver.add(zone["Parra"] == zone["Quinn"])

# Condition 4: Stuckey and Udall work in the same sales zone as each other.
solver.add(zone["Stuckey"] == zone["Udall"])

# Condition 5: There are more of the sales representatives working in Zone 3 than in Zone 2.
# Count reps in Zone 3 and Zone 2
zone3_count = Sum([If(zone[r] == 3, 1, 0) for r in reps])
zone2_count = Sum([If(zone[r] == 2, 1, 0) for r in reps])
solver.add(zone3_count > zone2_count)

# Now evaluate each option.
# Each option gives a list of reps that are supposed to be in Zone 3.
# We need to check if there exists a complete assignment consistent with the option.
# The option says "complete and accurate list of the sales representatives working in Zone 3".
# So the reps listed are exactly those in Zone 3, and all other reps are NOT in Zone 3.

options = {
    "A": ["Kim", "Mahr"],
    "B": ["Kim", "Tiao"],
    "C": ["Parra", "Quinn"],
    "D": ["Stuckey", "Tiao", "Udall"],
    "E": ["Parra", "Quinn", "Stuckey", "Udall"]
}

found_options = []

for letter, zone3_list in options.items():
    solver.push()
    # The listed reps must be in Zone 3
    for r in zone3_list:
        solver.add(zone[r] == 3)
    # All other reps must NOT be in Zone 3
    for r in reps:
        if r not in zone3_list:
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