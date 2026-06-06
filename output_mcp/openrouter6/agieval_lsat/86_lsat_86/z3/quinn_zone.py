from z3 import *

# BENCHMARK_MODE: ON (problem is guaranteed solvable)
BENCHMARK_MODE = True

solver = Solver()

# Define persons
persons = ["Kim", "Mahr", "Parra", "Quinn", "Stuckey", "Tiao", "Udall"]
zone = {p: Int(p) for p in persons}

# Domain constraints: zones are 1, 2, or 3
for p in persons:
    solver.add(zone[p] >= 1, zone[p] <= 3)

# Base constraints
# 1. Either Parra or Tiao (but not both) works in Zone 1.
solver.add(Or(And(zone["Parra"] == 1, zone["Tiao"] != 1),
              And(zone["Tiao"] == 1, zone["Parra"] != 1)))

# 2. Either Tiao or Udall (but not both) works in Zone 2.
solver.add(Or(And(zone["Tiao"] == 2, zone["Udall"] != 2),
              And(zone["Udall"] == 2, zone["Tiao"] != 2)))

# 3. Parra and Quinn work in the same sales zone.
solver.add(zone["Parra"] == zone["Quinn"])

# 4. Stuckey and Udall work in the same sales zone.
solver.add(zone["Stuckey"] == zone["Udall"])

# 5. More representatives in Zone 3 than in Zone 2.
# Count how many are in zone 3 and zone 2.
count3 = Sum([If(zone[p] == 3, 1, 0) for p in persons])
count2 = Sum([If(zone[p] == 2, 1, 0) for p in persons])
solver.add(count3 > count2)

# Now evaluate each multiple choice option.
# We want to find the person X such that Quinn cannot work in the same zone as X.
# That is, adding zone["Quinn"] == zone[X] makes the problem unsatisfiable.
options = [("A", "Kim"), ("B", "Mahr"), ("C", "Stuckey"), ("D", "Tiao"), ("E", "Udall")]
impossible = []

for letter, person in options:
    solver.push()
    solver.add(zone["Quinn"] == zone[person])
    if solver.check() == unsat:
        impossible.append(letter)
    solver.pop()

# Determine the answer
if len(impossible) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible[0]}")
elif len(impossible) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {impossible}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")