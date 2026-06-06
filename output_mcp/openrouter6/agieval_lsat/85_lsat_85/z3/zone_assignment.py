from z3 import *

# Define people and their zone variables
people = ["Kim", "Mahr", "Parra", "Quinn", "Stuckey", "Tiao", "Udall"]
zone = {p: Int(f"zone_{p}") for p in people}

solver = Solver()

# Each zone must be 1, 2, or 3
for p in people:
    solver.add(zone[p] >= 1, zone[p] <= 3)

# Constraint 1: Either Parra or Tiao (but not both) works in Zone 1.
solver.add( (zone["Parra"] == 1) != (zone["Tiao"] == 1) )

# Constraint 2: Either Tiao or Udall (but not both) works in Zone 2.
solver.add( (zone["Tiao"] == 2) != (zone["Udall"] == 2) )

# Constraint 3: Parra and Quinn work in the same zone.
solver.add(zone["Parra"] == zone["Quinn"])

# Constraint 4: Stuckey and Udall work in the same zone.
solver.add(zone["Stuckey"] == zone["Udall"])

# Constraint 5: More reps in Zone 3 than Zone 2.
count_zone3 = Sum([If(zone[p] == 3, 1, 0) for p in people])
count_zone2 = Sum([If(zone[p] == 2, 1, 0) for p in people])
solver.add(count_zone3 > count_zone2)

# Define the options as lists of people in Zone 3
options = {
    "A": ["Kim", "Mahr"],
    "B": ["Kim", "Tiao"],
    "C": ["Parra", "Quinn"],
    "D": ["Stuckey", "Tiao", "Udall"],
    "E": ["Parra", "Quinn", "Stuckey", "Udall"]
}

found_options = []
for letter, opt_people in options.items():
    solver.push()
    # For each person in the option, they must be in Zone 3
    for p in opt_people:
        solver.add(zone[p] == 3)
    # For each person not in the option, they must NOT be in Zone 3
    for p in people:
        if p not in opt_people:
            solver.add(zone[p] != 3)
    # Check satisfiability
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output according to the required skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")