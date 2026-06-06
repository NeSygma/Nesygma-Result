from z3 import *

solver = Solver()

# Seven sales representatives
reps = ["Kim", "Mahr", "Parra", "Quinn", "Stuckey", "Tiao", "Udall"]

# Each works in exactly one of zones 1, 2, or 3
zone = {r: Int(f"zone_{r}") for r in reps}

for r in reps:
    solver.add(zone[r] >= 1, zone[r] <= 3)

# Condition 1: Either Parra or Tiao (but not both) works in Zone 1.
# Exactly one of them is in zone 1.
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

# Now evaluate each option: "Quinn CANNOT work in the same sales zone as which one of the following?"
# For each option X, we check if it's possible for Quinn and X to be in the same zone.
# The one that is IMPOSSIBLE (unsat) is the answer.

found_options = []

# Option A: Kim
opt_a = (zone["Quinn"] == zone["Kim"])
# Option B: Mahr
opt_b = (zone["Quinn"] == zone["Mahr"])
# Option C: Stuckey
opt_c = (zone["Quinn"] == zone["Stuckey"])
# Option D: Tiao
opt_d = (zone["Quinn"] == zone["Tiao"])
# Option E: Udall
opt_e = (zone["Quinn"] == zone["Udall"])

for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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