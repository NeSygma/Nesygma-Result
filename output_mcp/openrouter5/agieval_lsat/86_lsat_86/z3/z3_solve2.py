from z3 import *

solver = Solver()

# Seven sales representatives
reps = ["Kim", "Mahr", "Parra", "Quinn", "Stuckey", "Tiao", "Udall"]

# Each works in exactly one of zones 1, 2, or 3
zone = {r: Int(f"zone_{r}") for r in reps}

for r in reps:
    solver.add(zone[r] >= 1, zone[r] <= 3)

# Condition 1: Either Parra or Tiao (but not both) works in Zone 1.
solver.add(If(zone["Parra"] == 1, 1, 0) + If(zone["Tiao"] == 1, 1, 0) == 1)

# Condition 2: Either Tiao or Udall (but not both) works in Zone 2.
solver.add(If(zone["Tiao"] == 2, 1, 0) + If(zone["Udall"] == 2, 1, 0) == 1)

# Condition 3: Parra and Quinn work in the same sales zone as each other.
solver.add(zone["Parra"] == zone["Quinn"])

# Condition 4: Stuckey and Udall work in the same sales zone as each other.
solver.add(zone["Stuckey"] == zone["Udall"])

# Condition 5: There are more of the sales representatives working in Zone 3 than in Zone 2.
zone3_count = Sum([If(zone[r] == 3, 1, 0) for r in reps])
zone2_count = Sum([If(zone[r] == 2, 1, 0) for r in reps])
solver.add(zone3_count > zone2_count)

# Let's first find a valid model to understand the constraints
print("Checking for a valid model...")
result = solver.check()
if result == sat:
    m = solver.model()
    for r in reps:
        print(f"{r}: Zone {m[zone[r]]}")
else:
    print("No valid model found initially")
    print("Let's debug...")

# The question: "Quinn CANNOT work in the same sales zone as which one of the following?"
# This means: for which X is it IMPOSSIBLE (unsat) that Quinn and X share a zone?
# We need to find the option that is UNSAT when we add the constraint that they share a zone.

# Let me re-examine. The question asks which one Quinn CANNOT work with.
# So we test each option: can Quinn and X be in the same zone?
# The one that returns UNSAT is the answer.

solver2 = Solver()
for r in reps:
    solver2.add(zone[r] >= 1, zone[r] <= 3)

solver2.add(If(zone["Parra"] == 1, 1, 0) + If(zone["Tiao"] == 1, 1, 0) == 1)
solver2.add(If(zone["Tiao"] == 2, 1, 0) + If(zone["Udall"] == 2, 1, 0) == 1)
solver2.add(zone["Parra"] == zone["Quinn"])
solver2.add(zone["Stuckey"] == zone["Udall"])
zone3_count2 = Sum([If(zone[r] == 3, 1, 0) for r in reps])
zone2_count2 = Sum([If(zone[r] == 2, 1, 0) for r in reps])
solver2.add(zone3_count2 > zone2_count2)

found_options = []
for letter, name in [("A", "Kim"), ("B", "Mahr"), ("C", "Stuckey"), ("D", "Tiao"), ("E", "Udall")]:
    solver2.push()
    solver2.add(zone["Quinn"] == zone[name])
    res = solver2.check()
    print(f"Option {letter} ({name}): {res}")
    if res == sat:
        found_options.append(letter)
    solver2.pop()

print(f"Found options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")