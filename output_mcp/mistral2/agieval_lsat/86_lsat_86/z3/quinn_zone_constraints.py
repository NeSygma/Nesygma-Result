from z3 import *

# Declare symbolic variables for each sales representative's zone
# We represent zones as integers: 1, 2, 3
zones = {
    "Kim": Int("Kim"),
    "Mahr": Int("Mahr"),
    "Parra": Int("Parra"),
    "Quinn": Int("Quinn"),
    "Stuckey": Int("Stuckey"),
    "Tiao": Int("Tiao"),
    "Udall": Int("Udall"),
}

# Each representative works in exactly one of the three zones
solver = Solver()
for rep in zones:
    solver.add(Or(zones[rep] == 1, zones[rep] == 2, zones[rep] == 3))

# Condition 1: Either Parra or Tiao (but not both) works in Zone 1
solver.add(Or(And(zones["Parra"] == 1, zones["Tiao"] != 1), 
              And(zones["Tiao"] == 1, zones["Parra"] != 1)))

# Condition 2: Either Tiao or Udall (but not both) works in Zone 2
solver.add(Or(And(zones["Tiao"] == 2, zones["Udall"] != 2), 
              And(zones["Udall"] == 2, zones["Tiao"] != 2)))

# Condition 3: Parra and Quinn work in the same sales zone
solver.add(zones["Parra"] == zones["Quinn"])

# Condition 4: Stuckey and Udall work in the same sales zone
solver.add(zones["Stuckey"] == zones["Udall"])

# Condition 5: There are more representatives in Zone 3 than in Zone 2
# Count the number of representatives in Zone 2 and Zone 3
zone_counts = {
    1: Sum([If(zones[rep] == 1, 1, 0) for rep in zones]),
    2: Sum([If(zones[rep] == 2, 1, 0) for rep in zones]),
    3: Sum([If(zones[rep] == 3, 1, 0) for rep in zones]),
}
solver.add(zone_counts[3] > zone_counts[2])

# Base constraints are set. Now evaluate each option to see if Quinn CANNOT work in the same zone as the option.
# We need to check for each option (A, B, C, D, E) whether it is possible for Quinn to be in the same zone as that option.
# If it is NOT possible (i.e., the solver returns unsat for that option), then that option is the answer.

found_options = []

# Option A: Quinn cannot work in the same zone as Kim
solver.push()
solver.add(zones["Quinn"] == zones["Kim"])
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Quinn cannot work in the same zone as Mahr
solver.push()
solver.add(zones["Quinn"] == zones["Mahr"])
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Quinn cannot work in the same zone as Stuckey
solver.push()
solver.add(zones["Quinn"] == zones["Stuckey"])
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Quinn cannot work in the same zone as Tiao
solver.push()
solver.add(zones["Quinn"] == zones["Tiao"])
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Quinn cannot work in the same zone as Udall
solver.push()
solver.add(zones["Quinn"] == zones["Udall"])
if solver.check() == sat:
    found_options.append("E")
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